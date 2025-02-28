import json
from datetime import date
import rich
from rich import print
from rich.console import Console
from rich.theme import Theme


from typing import List, Dict

custom_theme = Theme({
    "menu": "cyan",
    "info": "magenta",
    "warning": "yellow",
    "danger": "bold red"
})
console = Console(theme=custom_theme)

class User:
    def __init__(self, name: str, pin: str):
        self.name = name
        self.pin = pin

class CalorieTracker:
    def __init__(self, user: User):
        self.user = user
        self.calorie_daily_target = 2000  # Default value
        self.entries: List[Dict] = []

    def set_calorie_target(self):
        while True:
            try:
                self.calorie_daily_target = int(input("Set your daily calorie target: "))
                if self.calorie_daily_target <= 0:
                    raise ValueError
                self.save_calorie_target()
                print(f"Daily calorie target set to {self.calorie_daily_target}.")
                break
            except ValueError:
                console.print("Please enter a valid number.", style="warning")

    def add_calorie_entry(self):
        while True:
            try:
                today = date.today().isoformat()
                calories = int(input("Add to today's entry: "))
                if calories < 0:
                    raise ValueError
                self.entries.append({"date": today, "calories": calories})
                self.save_entries()
                print(f"Entry added: {calories} calories on {today}")
                break
            except ValueError:
                console.print("Please enter a valid number.", style="warning")

    def view_entries(self):
        if not self.entries:
            print("No entries yet.")
            return

        print("\nCalorie Entries:")
        for entry in self.entries:
            print(f"{entry['date']}: {entry['calories']} calories")
        remaining_calories = self.get_remaining_calories()
        print(f"\nRemaining calories: {remaining_calories}")

    def get_remaining_calories(self):
        consumed_calories = sum(entry["calories"] for entry in self.entries)
        return self.calorie_daily_target - consumed_calories

    def save_calorie_target(self):
        data = {
            "name": self.user.name,
            "calorie_daily_target": self.calorie_daily_target,
            "date": date.today().isoformat()
        }
        try:
            with open("calorie_target.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving calorie target: {e}")

    def save_entries(self):
        data = {
            "name": self.user.name,
            "entries": self.entries
        }
        try:
            with open("calorie_entries.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            console.print(f"Error saving entries: {e}", style="danger")

    @classmethod
    def load_calorie_target(cls, user: User):
        try:
            with open("calorie_target.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if data["name"] == user.name:
                    return data["calorie_daily_target"]
        except (FileNotFoundError, json.JSONDecodeError):
            return 2000

    @classmethod
    def load_entries(cls, user: User):
        try:
            with open("calorie_entries.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if data["name"] == user.name:
                    return data["entries"]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

def verify_user():
    name = input("Enter your name: ")
    pin = input("Enter your PIN: ")
    user = User(name, pin)
    tracker = CalorieTracker(user)
    tracker.calorie_daily_target = CalorieTracker.load_calorie_target(user)
    tracker.entries = CalorieTracker.load_entries(user)
    return tracker

def display_menu(tracker: CalorieTracker):
    while True:
        console.print("\nChoose an option:")
        console.print("1. Set calorie target", style="menu")
        console.print("2. Add calorie entry", style="menu")
        console.print("3. View entries & remaining calories", style="menu")
        console.print("4. Help", style="menu")
        console.print("5. Quit", style="info")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            tracker.set_calorie_target()
        elif choice == "2":
            tracker.add_calorie_entry()
        elif choice == "3":
            tracker.view_entries()
        elif choice == "4":
            display_help()
        elif choice == "5":
            console.print("Thank you for using the app, have a great day!", style="info")
            break
        else:
            print("Invalid choice. Please try again.")

def display_help():
    help_text = """
    Calorie Tracker Help

    Welcome to the Calorie Tracker app! This tool helps you monitor your daily calorie intake.

    How to Use:
    1. Set your daily calorie target
    2. Add calorie entries throughout the day
    3. View your entries and remaining calories

    Tips for Effective Tracking:
    - Aim for consistency in your logging habits
    - For incorrect calculations, check if you have entered the correct numbers in the correct format.

    Need More Help?
    Contact us at support@calorietracker.com
    """
    print(help_text)
    input("Press Enter to return to the main menu.")

def main():
    tracker = verify_user()
    display_menu(tracker)

if __name__ == "__main__":
    main()
