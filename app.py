from flask import Flask, render_template, request
import random
import os

def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        return 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        return 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

def calculate_macros(bmr, activity_level):
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    total_calories = bmr * activity_multipliers.get(activity_level, 1.2)
    protein = (total_calories * 0.3) / 4
    fats = (total_calories * 0.25) / 9
    carbs = (total_calories * 0.45) / 4
    
    return total_calories, protein, fats, carbs

def generate_meal_plan(protein, fats, carbs, diet):
    food_database = {
        "standard": {
            "protein": ["Chicken Breast", "Eggs", "Tofu", "Salmon", "Greek Yogurt"],
            "fats": ["Avocado", "Almonds", "Olive Oil", "Peanut Butter", "Cheese"],
            "carbs": ["Oats", "Brown Rice", "Quinoa", "Sweet Potato", "Banana"]
        },
        "vegetarian": {
            "protein": ["Tofu", "Lentils", "Greek Yogurt", "Chickpeas", "Cottage Cheese"],
            "fats": ["Avocado", "Almonds", "Olive Oil", "Peanut Butter", "Cheese"],
            "carbs": ["Oats", "Brown Rice", "Quinoa", "Sweet Potato", "Banana"]
        },
        "keto": {
            "protein": ["Chicken Breast", "Salmon", "Eggs", "Beef", "Pork"],
            "fats": ["Avocado", "Olive Oil", "Butter", "Cheese", "Almonds"],
            "carbs": ["Spinach", "Zucchini", "Mushrooms", "Broccoli", "Cauliflower"]
        }
    }
    
    selected_foods = food_database.get(diet, food_database["standard"])
    
    meal_plan = {
        "Breakfast": [random.choice(selected_foods["protein"]), random.choice(selected_foods["carbs"])],
        "Lunch": [random.choice(selected_foods["protein"]), random.choice(selected_foods["fats"]), random.choice(selected_foods["carbs"])],
        "Dinner": [random.choice(selected_foods["protein"]), random.choice(selected_foods["fats"]), random.choice(selected_foods["carbs"])],
        "Snack": [random.choice(selected_foods["protein"]), random.choice(selected_foods["fats"])]
    }
    
    return meal_plan

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        activity_level = request.form['activity_level']
        diet = request.form['diet']
        
        bmr = calculate_bmr(weight, height, age, gender)
        total_calories, protein, fats, carbs = calculate_macros(bmr, activity_level)
        meal_plan = generate_meal_plan(protein, fats, carbs, diet)
        
        return render_template('result.html', calories=total_calories, protein=protein, fats=fats, carbs=carbs, meal_plan=meal_plan)
    
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
