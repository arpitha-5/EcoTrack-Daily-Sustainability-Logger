🌱 EcoTrack – Daily Sustainability Logger

EcoTrack is a Python-based desktop application that helps users log, manage, and visualize their daily sustainable activities.
It is built using Tkinter for the GUI, tkcalendar for date selection, and Matplotlib for generating category-based pie chart summaries.

All user entries are saved locally in a JSON file for persistent tracking.

🖥️ Features

📝 Add New Entry – Log eco-friendly activities with details such as date, category, impact, and notes.

✏️ Update Existing Entries – Select and modify an entry directly from the table.

🗑️ Delete Entries – Remove unnecessary or old records easily.

📊 View Summary Chart – Generate a category-based pie chart summarizing your sustainable activities.

💾 Automatic Data Storage – All entries are stored in a local JSON file (data/ecotrack_data.json).

🎨 Modern User Interface – Uses ttk styling and color themes for a clean, green design.

📁 Project Structure
EcoTrack/
│
├── data/
│   └── ecotrack_data.json        # Auto-created JSON file for data storage
│
├── ecotrack_app.py               # Main application file (your provided code)
│
└── README.md                     # Documentation file

⚙️ How to Run
1️⃣ Prerequisites

Make sure Python 3.x is installed on your system.
You can verify using:

python --version

2️⃣ Install Required Packages

Install the necessary dependencies:

pip install tkcalendar matplotlib


(Tkinter usually comes pre-installed with Python.)

3️⃣ Run the Application

Navigate to the folder containing your code and execute:

python ecotrack_app.py

🧩 Application Overview
🪴 Add / Update / Delete Activity

Select a date using the DateEntry calendar.

Enter an activity name, choose a category, set the impact level, and add optional notes.

Click “➕ Add Entry” to save the record.

Select an existing record from the table and click “✏ Update Selected” to edit it.

To cancel editing, click “↩ Cancel Edit”.

To remove an entry, click “🗑 Delete Entry”.

📊 View Summary

Click “📊 View Summary” to open a Matplotlib pie chart displaying the percentage of entries per category.

🚀 Future Enhancements

Export data as .csv or .xlsx

Add filtering by date range or category

Display line/bar charts for trends over time

Cloud backup or sync with Google Sheets








