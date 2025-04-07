# nutrition_tracker_lib/tracker.py
import requests
from django.conf import settings
from datetime import datetime

class NutritionTracker:
    def __init__(self):
        self.meal_log = []
        self.water_log = []
        self.weight_log = []
        self.api_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        self.api_key = settings.USDA_API_KEY

    def fetch_nutrition_data(self, food_name):
        """Fetch nutrition data for a given food item from an external API."""
        params = {
            'query': food_name,
            'api_key': self.api_key
        }
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            if "foods" in data and data["foods"]:
                food = data["foods"][0]
                nutrients = {nutrient["nutrientName"]: nutrient["value"] for nutrient in food["foodNutrients"]}
                return {
                    "name": food["description"],
                    "calories": nutrients.get("Energy", 0),
                    "protein": nutrients.get("Protein", 0),
                    "carbs": nutrients.get("Carbohydrate, by difference", 0),
                    "fats": nutrients.get("Total lipid (fat)", 0),
                    "sugar": nutrients.get("Sugars, total", 0),
                    "fiber": nutrients.get("Fiber, total dietary", 0)
                }
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def log_meal(self, food_name, calories, protein, carbs, fats):
        entry = {
            "food": food_name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.meal_log.append(entry)
        return entry

    def log_water(self, amount_ml):
        entry = {"amount_ml": amount_ml, "date": datetime.now().strftime("%Y-%m-%d")}
        self.water_log.append(entry)
        return entry

    def log_weight(self, weight):
        entry = {"weight": weight, "date": datetime.now().strftime("%Y-%m-%d")}
        self.weight_log.append(entry)
        return entry

    def get_meal_summary(self):
        total_calories = sum(meal["calories"] for meal in self.meal_log)
        return {"total_meals": len(self.meal_log), "total_calories": total_calories}

    def get_water_summary(self):
        total_water = sum(entry["amount_ml"] for entry in self.water_log)
        return {"total_entries": len(self.water_log), "total_water_ml": total_water}

    def get_weight_progress(self):
        return sorted(self.weight_log, key=lambda x: x["date"], reverse=True)