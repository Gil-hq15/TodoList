# 📝 **To-Do List App with Flask**

The **To-Do List App** is a feature-rich web application developed with Flask. It helps users manage tasks efficiently while integrating additional functionality like **OAuth login**, **NASA Astronomy Picture of the Day (APOD)** display, and **task prioritization**. The app supports dynamic task management and robust user authentication to ensure a secure and personalized experience.

---

## 🌟 **Key Features**

- **User Authentication:**
  Secure login and registration via form-based authentication or Google OAuth.

- **Task Management:** 
  - Create, update, and delete tasks.  
  - Assign and enforce priorities: **High**, **Medium**, or **Low**.  
  - Sort tasks by creation date.  
  - Error handling for invalid or empty tasks.

- **NASA APOD Integration:** 
  Fetches and displays the **Astronomy Picture of the Day** for a random date upon successful login.

- **Load and Performance Testing:**
  Built-in load tests using Locust to evaluate performance under concurrent usage.

---

## 🛠️ **Project Structure**

```plaintext
.
├── app/                    # Core Flask application
│   ├── __init__.py         # App factory and extensions initialization
│   ├── models.py           # Database models (User and Todo)
│   ├── routes/             # Modularized route definitions
│   ├── static/             # Static files (CSS, JS, images)
│   └── templates/          # HTML templates for the app
├── config.py               # Configuration classes (development, testing, production)
├── run.py                  # App runner
├── requirements.txt        # Python dependencies
├── tests/                  # Unit, integration, acceptance, and performance tests
└── README.md               # Project documentation
```

---

## 🛠️ **Project Structure**

### Prerequisites
- Python 3.8 or higher.
- Git installed on your system.
- A virtual environment to manage dependencies.

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/to_do_list_app.git
    cd to_do_list_app
    ```

2. **Create and activate a virtual environment:**

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Rename `.env.example` to `.env`.
   - Fill in the required variables like `SECRET_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `NASA_API_KEY`.

5. **Initialize the database:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6. **Run the application:**

    ```bash
    flask run
    ```

   The app will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🧪 Testing

### Functional Tests
Run unit and integration tests using pytest to validate core functionalities like user authentication, task operations, and API integrations:

1. Ensure the virtual environment is active.
2. Run the tests:

    ```bash
    pytest
    ```

   Coverage reports are generated in both HTML and console formats.

### Performance Tests
Use Locust to simulate multiple users performing operations and evaluate application performance:

1. Ensure the app is running locally.
2. Run Locust:

    ```bash
    locust -f tests/performance/load_testing.py
    ```

   Open [http://127.0.0.1:8089](http://127.0.0.1:8089) to configure test parameters and view metrics.

---

## ⚙️ Configuration

The application uses environment variables for sensitive information. Here’s an example `.env` file:

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///dev.db
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
NASA_API_KEY=your_nasa_api_key
```

---

## 🚀 API Integration: NASA APOD

Upon successful login, the app fetches the Astronomy Picture of the Day (APOD) using the NASA APOD API. This feature demonstrates how external APIs can enrich user experiences.

Example API usage in the app:

```python
response = requests.get(
    'https://api.nasa.gov/planetary/apod',
    params={'api_key': nasa_api_key, 'date': random_date}
)
```

---

## 📁 Database Models

- **User**: Stores user information with hashed passwords for security.
- **Todo**: Tracks user-specific tasks, priorities, and timestamps.

---

## 🔑 Security Features

- **Secure Passwords**: Passwords are hashed using werkzeug.security.
- **CSRF Protection**: Ensured via Flask’s session-based approach.
- **OAuth 2.0**: Implements Google OAuth for secure third-party login.

--

## 🧑‍💻 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.