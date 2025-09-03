# Momentum — ***small*** steps, ***big*** changes
Momentum is a simple and fully-centered command-line interface (CLI) for tracking your daily habits. It helps you build and maintain a consistent routine without any distractions. Built with **Python** and **SQLite3**, this CLI provides a clean and intuitive experience right in your terminal.

## ✨ Features
- **Add & Remove Habits**: Easily create new habits to track or remove old ones you no longer need.  
- **Log Daily Progress**: Mark habits as completed (✅) or not (❌) for the current day.  
- **View History**: See a detailed log of your habit progress over time.  
- **List All Habits**: Get a quick overview of all the habits you're tracking.  
- **Centered Interface**: A minimalist design that centers all output and input, keeping you focused on your goals.  

## 🛠️ Installation
### Prerequisites
- Python **3.6+**  
- [`rich`](https://github.com/Textualize/rich) library  

Install Rich:
```bash
pip install rich
```

## Clone the Repository
```bash
git clone https://github.com/blu3OceanWaves/Momentum
cd Momentum
```

## Run the Application
```bash
chmod +x momentum
./momentum
```

## 🧭 How to Use
Momentum’s interface is designed to be straightforward. When you run the script, you’ll be greeted with a main menu. Simply enter the number corresponding to the action you want to perform.

### Main Menu Options:
- Add Habit: Enter a name for a new habit you want to track.
- View History: See a chronological log for a specific habit.
- Log Habit: Mark a habit as done for the current day.
- Remove Habit: Delete a habit from your tracker.
- List Habits: Display all your active habits.
- Quit: Exit the application.

## 📂 File Structure
```bash
momentum/
├── momentum      # The main script containing all logic for the CLI
└── momentum.db   # The SQLite database file (automatically done in same dir)
```

## 🗫 Contributing
If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request.

