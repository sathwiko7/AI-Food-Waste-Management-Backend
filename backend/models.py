from sqlalchemy import Column, Integer, String , DateTime
from database import Base
from datetime import datetime




# -------------------------
# User Table
# -------------------------
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


# -------------------------
# Food Listing Table
# -------------------------
class FoodListing(Base):
    __tablename__ = "food_listings"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)
    quantity = Column(String)
    location = Column(String)
    donor_id = Column(Integer)
    status = Column(String, default="available")
    claimed_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    expiry_estimate = Column(String, nullable=True)