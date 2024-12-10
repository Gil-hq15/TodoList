## 🧪 Testing

### Functional Tests
Run unit and integration tests using pytest to validate core functionalities like user authentication, task operations, and API integrations:

1. Ensure the virtual environment is active.
2. Run the tests:

    ```bash
    pytest
    ```

   Coverage reports are generated in both HTML and console formats.

### Acceptance Tests with Playwright

Run acceptance tests with Playwright to validate end-to-end functionalities and ensure the system meets user requirements:

1. Ensure the virtual environment is active.
2. Install Playwright dependencies if not done already:

    ```bash
    pip install playwright
    playwright install
    ```

3. Run the acceptance tests:

    ```bash
    pytest --browser=chrome
    ```

4. Playwright will execute the end-to-end tests in a real browser to validate features like user login, task management, and interaction with the database.

    Coverage reports will be displayed in the terminal, and if configured, an HTML report will be generated for a detailed view of the test results.

### Performance Tests
Use Locust to simulate multiple users performing operations and evaluate application performance:

1. Ensure the app is running locally.
2. Set virtual environment for locust dependencies, and run Locust:

    ```bash
    python3 -m venv locust-env
    source locust-env/bin/activate
    pip install -r load_requirements.txt
    locust -f tests/performance/load_testing.py
    ```

   Open [http://127.0.0.1:8089](http://127.0.0.1:8089) to configure test parameters and view metrics.

---