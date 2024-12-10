## 🛠️ **Instalation**

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
