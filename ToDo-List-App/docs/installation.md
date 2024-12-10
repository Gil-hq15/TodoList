# Installation and Setup

To get the To-Do List App running on your local machine, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/to_do_list_app.git
    cd to_do_list_app
    ```

2. **Set up a virtual environment** and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the environment variables**:
    - Rename `.env.example` to `.env` and update the values.
    
5. **Run the application**:
    ```bash
    flask run
    ```

Visit `http://127.0.0.1:5000` to view the app.