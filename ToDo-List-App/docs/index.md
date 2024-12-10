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

## 📁 Database Models

- **User**: Stores user information with hashed passwords for security.
- **Todo**: Tracks user-specific tasks, priorities, and timestamps.

---

## 🔑 Security Features

- **Secure Passwords**: Passwords are hashed using werkzeug.security.
- **CSRF Protection**: Ensured via Flask’s session-based approach.
- **OAuth 2.0**: Implements Google OAuth for secure third-party login.

---