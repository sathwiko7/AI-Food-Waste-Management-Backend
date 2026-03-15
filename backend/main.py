from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from security import create_access_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security import hash_password, verify_password
from security import verify_password
import schemas
from ai_utils import predict_expiry
from datetime import datetime, timedelta
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware

from ai_utils import predict_expiry

app = FastAPI()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

models.Base.metadata.create_all(bind=engine)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET CURRENT USER FROM TOKEN
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials
    user_id = verify_token(token)

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# REGISTER
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return  new_user


# LOGIN

@app.post("/login")
def login_user(
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# DASHBOARD
@app.get("/dashboard")
def dashboard(current_user: models.User = Depends(get_current_user)):

    if current_user.role == "donor":
        return {"dashboard": "Donor Dashboard"}

    elif current_user.role == "ngo":
        return {"dashboard": "NGO Dashboard"}

    else:
        return {"dashboard": "Admin Dashboard"}


# VIEW AVAILABLE FOOD (NGO ONLY)
@app.get("/available-food", response_model=list[schemas.FoodResponse])
def view_available_food(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "ngo":
        raise HTTPException(status_code=403, detail="Only NGOs can view food")

    # Food older than 6 hours is considered expired
    expiry_time = datetime.utcnow() - timedelta(hours=6)

    food_items = db.query(models.FoodListing).filter(
        models.FoodListing.status == "available",
        models.FoodListing.created_at > expiry_time
    ).order_by(models.FoodListing.created_at.desc()).all()

    return food_items


# ADD FOOD (DONOR ONLY)
@app.post("/add-food", response_model=schemas.FoodResponse)
def add_food(
    food: schemas.FoodCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "donor":
        raise HTTPException(status_code=403, detail="Only donors can add food")

    expiry = predict_expiry(food.food_name)

    food_item = models.FoodListing(
        food_name=food.food_name,
        quantity=food.quantity,
        location=food.location,
        donor_id=current_user.id,
        expiry_estimate=expiry
    )

    db.add(food_item)
    db.commit()
    db.refresh(food_item)

    return food_item

# CLAIM FOOD (NGO)
@app.post("/claim-food")
def claim_food(
    food_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "ngo":
        raise HTTPException(status_code=403, detail="Only NGOs can claim food")

    food = db.query(models.FoodListing).filter(
        models.FoodListing.id == food_id
    ).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    if food.status == "claimed":
        raise HTTPException(status_code=400, detail="Food already claimed")

    food.status = "claimed"
    food.claimed_by = current_user.id

    db.commit()

    return {"message": "Food claimed successfully"}


# MY DONATIONS
@app.get("/my-donations")
def my_donations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "donor":
        raise HTTPException(status_code=403, detail="Only donors")

    foods = db.query(models.FoodListing).filter(
        models.FoodListing.donor_id == current_user.id
    ).all()

    return foods


# MY CLAIMS
@app.get("/my-claims")
def my_claims(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "ngo":
        raise HTTPException(status_code=403, detail="Only NGOs")

    foods = db.query(models.FoodListing).filter(
        models.FoodListing.claimed_by == current_user.id
    ).all()

    return foods



#where i can see all the total countings
@app.get("/admin-stats")
def admin_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Only admin can access
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can view dashboard"
        )

    total_users = db.query(models.User).count()

    total_food = db.query(models.FoodListing).count()

    total_claimed = db.query(models.FoodListing).filter(
        models.FoodListing.status == "claimed"
    ).count()

    total_available = db.query(models.FoodListing).filter(
        models.FoodListing.status == "available"
    ).count()

    return {
        "total_users": total_users,
        "total_food_listings": total_food,
        "claimed_food": total_claimed,
        "available_food": total_available
    }




@app.get("/search-food")
def search_food(
    location: str,
    db: Session = Depends(get_db)
):

    foods = db.query(models.FoodListing).filter(
        models.FoodListing.location == location,
        models.FoodListing.status == "available"
    ).all()

    if not foods:
        return {"message": "No food found in this location"}

    return foods




@app.post("/predict-expiry")
def predict(food_item: str):
    days = predict_expiry(food_item)
    return {
        "food_item": food_item,
        "predicted_expiry_days": days
    }


@app.get("/nearby-food")
def get_nearby_food(
    location: str,
    db: Session = Depends(get_db)
):
    
    foods = db.query(models.FoodListing).filter(
        models.FoodListing.location.ilike(f"%{location}%")
    ).all()

    return foods