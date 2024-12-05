# Habit Tracker API

A **Backend API** for a **Habit Tracking System**, designed for efficient tracking, monitoring, and analysis of personal habits and streaks.

## Built With:
- **FastAPI**: Framework for building fast, scalable APIs.
- **PostgreSQL**: Database management system.
- **Alembic** and **SQLAlchemy**: Tools for database migrations.
- **JSON Web Token (JWT)**: For secure user authentication and authorization.

## Features:
- User authentication and authorization.
- CRUD operations for habit management: create, update, delete habits.
- Streak tracking and detailed analytics for user insights.
- Secure JWT-based authentication.

## Installation:

1. **Clone the repository:**
   git clone https://github.com/myingineer/habit_tracker.git
   cd habit_tracker

2. **Set up a Virtual environment**
    Set up a virtual environment on your pc to run this project.
    This project was done using a mac, run this code in your terminal

        python -m venv yourvirtualenvironmentname

3. **Activate the virtual environment**
    Type this in your terminal

        yourvirtualenvironmentname\Scripts\activate 

4. **Install Dependencies**

        pip install -r requirements.txt

5. **Download and Setup a PostgreSQL Server**
    - Install PostgreSQL _if you do not have_
        [Click Here to Download](https://www.postgresql.org/download/)

    - Create a Server
    - Create a Database

6. **Set up the environment variables**
    Create a .env file in the root directory

        Add the following variables
        
            - DB_URL=_yourdburl_ postgres default localhost
            - DB_PORT=_yourdbport_ postgres default usually 5432
            - DB_PASSWORD=_yourdbpassword_
            - DB_USERNAME=_yourdbusername_
            - DB_NAME=_yourdbname_
            - SECRET_KEY = _yoursecretkey_
            - ALGORITHM = "HS256"
            - ACCESS_TOKEN_EXPIRE_MINUTES = 60
            - EMAIL_APP_PASSWORD= **see note below**
            - EMAIL_ADDRESS= **see note below**

7. **Run the migration to create all the tables**
    In the terminal, run this command

        alembic upgrade heads

8. **Add testing data to the respective tables**
    In the terminal, run this command

        python load_csv_to_db.py

#### INFO ---------------------------------------
    After the code in line 8 runs, you automatically have two users in the database with at least 4 weeks tracking data

            username: alexis, password: 123456789
            username:john, password: 123456789
Any of these user can be used to test the code
### -----------------------------------------------

9. **Run the code**
    In the terminal, run this command

        uvicorn app.main:app --reload


        The response should look like this 
            INFO:     Will watch for changes in these directories: ['/Users/pc_name/location_of_folder/folder_name']
            INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) _running on port **8000**_
            INFO:     Started reloader process [9952] using WatchFiles
            INFO:     Started server process [9954]
            INFO:     Waiting for application startup.
            INFO:     Application startup complete.

10. **API ENDPOINT's**
    To view all the endpoints and test out this API
    Navigate to
        http://127.0.0.1:8000/docs#/ in your browser _or_
        http://127.0.0.1:8000/redoc

    _make sure the port **8000** is the same as where your project is running on from point **9** above_


### **Note on Email App Password and Address**  
1. To use the email functionality for password resets or notifications, you will need an **email account** and an **app-specific password**.

- **Email Address**: This should be the email address you wish to use for sending emails (e.g., for password reset emails, for password reset confirmation, signup confirmation).

- **Email App Password**: For security reasons, many email providers (e.g., Gmail) require app-specific passwords instead of your regular email password when integrating with third-party apps. You can generate this password through your email provider's security settings.

For example:
- **Gmail**: Go to [Google Account Security Settings](https://myaccount.google.com/security)
            - Enable 2-Step Verification
            - Generate an app-specific password.

Add the generated **app password** and your **email address** in the `.env` file under the `EMAIL_APP_PASSWORD` and `EMAIL_ADDRESS` variables.

If you wish to **not** use the email functionality, fill a dummy data for the `EMAIL_APP_PASSWORD` and `EMAIL_ADDRESS` variables in your .env file

2. You would only be able to test all of the **Reset Password Functionality** if your set up and **email address** and **app password**

3. To test out the funtionality, you have to sign up on the API with a **working email address**

4. When you test the **streak update** endpoint, the **current streak count** would default to **1** as I do not intend to mark the streaks when due. The data in the csv folder is strictly intended to be a dummy data to test out the functionality. 
Since the project is being set up locally on your machine, you can tweak the data in the database locally to test out whatever function you wish to test.