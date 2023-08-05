# EgyptoPedia
#### Video Demo:  https://youtu.be/I1RmvDYD7z4
#### Description: An online guide to Egypt's mesmerizing attractions, designed to help visitors organize and plan their dream trip to Egypt.
#### Live Version (depoloyment): https://saifashrafhelmy.pythonanywhere.com/


## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Project Tree](#projecttree)



## Description
EgyptoPedia is a Flask-based web application that allows users to explore various attractions in Egypt, plan trips, and keep track of their visited attractions. It provides a user-friendly interface to register, log in, search for attractions by name or city, view attraction details, add attractions to a trip, and manage the trip itinerary.

## Installation

1. Clone the repository:
   git clone https://github.com/your-username/EgyptoPedia.git \
   cd EgyptoPedia

2. Create and activate a virtual environment: \
   python3 -m venv venv \
   source venv/bin/activate 

3. Install the required dependencies:
   pip install -r requirements.txt

4. Create the database and initialize tables:
   python app.py db init \
   python app.py db migrate \ 
   python app.py db upgrade \

5. Set environment variables by creating a .env file in the project root directory and adding the following line:
   my_secret_key=your_secret_key_here \
   Replace your_secret_key_here with a secret key of your choice. 

6. Run the application:
   python app.py \
   The application will be accessible at http://127.0.0.1:5000. 

## Usage
1. Register or log in to your account.
2. Explore attractions by searching for their names or filtering by city.
3. Click on an attraction to view its details.
4. Add attractions to your trip itinerary and specify visit dates.
5. View your trip itinerary to see the attractions you've added.
6. Remove attractions from your trip itinerary if needed.


## Features

- User authentication and registration.
- Search attractions by name or city.
- View detailed information about attractions.
- Add attractions to a trip itinerary with visit dates.
- View and manage your trip itinerary.
- Responsive design for various devices.
- Error handling and user-friendly messages.

## ProjectTree

📦EgyptoPedia
 ┣ 📂instance \
 ┃ ┗ 📜egy.db \
 ┣ 📂static \
 ┃ ┣ 📂bootstrap \
 ┃ ┃ ┣ 📜bootstrap.bundle.min.js \
 ┃ ┃ ┗ 📜bootstrap.min.css \
 ┃ ┣ 📜default.jpg \
 ┃ ┣ 📜eg_flag.ico \
 ┃ ┣ 📜eg_night.jpg \
 ┃ ┣ 📜home_styles.css\
 ┃ ┣ 📜main.css\
 ┃ ┣ 📜tl_style_v3.css\
 ┃ ┗ 📜view_page_styles.css\
 ┣ 📂templates\
 ┃ ┣ 📜attractions.html\
 ┃ ┣ 📜base.html\
 ┃ ┣ 📜home.html\
 ┃ ┣ 📜login_page.html\
 ┃ ┣ 📜register_page.html\
 ┃ ┣ 📜trip_final.html\
 ┃ ┗ 📜view_page.html\
 ┣ 📜.env\
 ┣ 📜app.py\
 ┣ 📜attractionsList.py\
 ┣ 📜attractionsListWithImages.py\
 ┣ 📜cities.py\
 ┣ 📜forms.py\
 ┣ 📜models.py\
 ┣ 📜README.md\
 ┣ 📜requirements.txt\
 ┗ 📜seed.py





