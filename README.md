# Smart Garden Planner

A smart gardening assistant designed to help users explore and understand plant care requirements with a clean and organized web interface. Built using **Python Flask**, this platform allows users to log in, browse categorized plant types, view care requirements, search and sort plants, and check out essential gardening tools.

> ⚠ *This is the initial version focused on web design and navigation. Machine Learning integration is planned for future upgrades.*

# Features (Current Version):

- **Beautifully Designed Home Page**
  - Clean layout introducing users to the idea of smart gardening.

- **User Authentication System**
  - Login / Sign up using email and password.
  - Data stored securely using **MongoDB**.

- **Plant Categories Page**
  - Displays plants grouped by their types.
  - Clicking a plant redirects to a dedicated **Plant Requirements** page.

- **Search & Sort Functionality**
  - Search for plants by name.
  - Sort plant listings for better navigation.

- **Gardening Tools Page**
  - Lists basic gardening tools with short descriptions.
  - Helpful for beginners starting their gardening journey.


# Future Improvements:

- **ML-based Smart Plant Suggestions**
  - Suggest plants based on user preferences, environment, and region.
  
- **Intelligent Garden Planning**
  - Predict water/light/fertilizer needs based on selected plants.

- **Plant Care Scheduler**
  - Notify users when to water based on seasons.

# Tech Stack:

- **Python (Flask)** : Backend server logic and routing 
- **HTML/CSS** : Frontend design 
- **MongoDB** : Database for storing user accounts 

# Project Structure:
```
SmartGardenPlanner/
│
├── app.py
│
├── static
│	  └── all images here
│
├── templates
│	  └── home.html
│	  └── main_page.html
│	  └── tools.html
│	  └── and all other plant's html pages
│
└── venv
```
