def predict_expiry(food_item: str):
    expiry_days = {
        "milk": 3,
        "bread": 4,
        "rice": 7,
        "vegetables": 5,
        "fruits": 4
    }

    return expiry_days.get(food_item.lower(), 3)
def predict_expiry(food_name: str):
    food = food_name.lower()

    if food in ["rice", "biryani", "pulao"]:
        return "6 hours"

    elif food in ["dosa", "idli", "chapati"]:
        return "8 hours"

    elif food in ["milk", "curd"]:
        return "4 hours"

    else:
        return "12 hours"