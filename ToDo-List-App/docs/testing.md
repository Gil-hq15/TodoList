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
    python3 -m venv locust-env
    source locust-env/bin/activate
    pip install -r load_requirements.txt
    locust -f tests/performance/load_testing.py
    ```

   Open [http://127.0.0.1:8089](http://127.0.0.1:8089) to configure test parameters and view metrics.

---