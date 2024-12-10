from locust import HttpUser, task, between
import random
import json
from locust.clients import HttpSession
from locust.exception import StopUser
import re

class ToDoUser(HttpUser):
    # Set the host for the Flask app (make sure the Flask app is running)
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)  # Wait time between tasks (in seconds)

    def on_start(self):
        """
            Simulates a login to the app by performing OAuth authentication.

            This method is called when the user starts the test. It attempts to log in using the OAuth login flow.
            - Calls the `login()` method to perform the login.
            - If the login is successful, stores the user ID and fetches the task IDs using the `get_task_ids()` method.
            - If the login fails, the test is stopped by raising a `StopUser` exception.

            Args:
                None.

            Returns:
                None. If login fails, the user is stopped from continuing the test.
        """
        # Perform OAuth login
        login_data = self.login()
        if login_data['status'] == 'ok':
            self.user_id = login_data['user_id']  # Store user_id after login
            self.task_ids = self.get_task_ids()  # Populate task_ids list after login
        else:
            raise StopUser("Login failed, stopping user")

    def login(self):
        """
            Simulates OAuth login by making a GET request to the /oauth-login route.

            This method performs the OAuth login flow, where a mock user is simulated.
            - Makes a GET request to `/oauth-login`.
            - Upon successful login (status code 200), simulates a callback using mock user data and makes a GET request to `/oauth-callback`.
            - If successful, returns a dictionary with the status 'ok' and a mock user ID.

            Args:
                None.

            Returns:
                dict: A dictionary with the login status and user ID.
                    - If login is successful, returns {'status': 'ok', 'user_id': 'mock_user_id'}.
                    - Otherwise, returns {'status': 'fail'}.
        """
        with self.client.get("/oauth-login", catch_response=True) as response:
            if response.status_code == 200:
                # Simulate a successful callback with mock user data
                oauth_data = {
                    "sub": "mock_user_id",  # Mock Google user ID
                    "name": "Test User",
                    "email": "testuser@example.com"
                }
                # Store the user ID and set the user_id in session
                login_response = self.client.get("/oauth-callback", params=oauth_data)
                if login_response.status_code == 200:
                    return {"status": "ok", "user_id": "mock_user_id"}
            return {"status": "fail"}


    def get_task_ids(self):
        """
            Fetches task IDs from the /index route by parsing the HTML response.

            This method is used to retrieve the IDs of the tasks displayed on the index page.
            - Makes a GET request to `/index` to load the tasks.
            - Uses a regular expression to extract task IDs from the HTML response.
            - Returns a list of task IDs as integers.

            Args:
                None.

            Returns:
                list: A list of integers representing the task IDs extracted from the response.
                    - If the request fails, returns an empty list.
        """

        with self.client.get("/index", catch_response=True) as response:
            if response.status_code == 200:
                # Use regex to find task IDs in the HTML table
                task_ids = re.findall(r'/delete/(\d+)', response.text)
                return [int(task_id) for task_id in task_ids]  # Convert IDs to integers
            response.failure("Failed to load task IDs")
            return []

    @task
    def create_task(self):
        """
            Simulates the creation of a new task by sending a POST request to the /index route.

            This method creates a new task with random content and priority.
            - Makes a POST request to `/index` to create a new task.
            - After the task is created successfully, updates the local list of task IDs.

            Args:
                None.

            Returns:
                None. If the task is successfully created, the task IDs are updated. If the creation fails, it logs the failure.
        """

        task_data = {
            "content": f"Task {random.randint(1, 1000)}",
            "priority": random.choice(["High", "Medium", "Low"])
        }
        with self.client.post("/index", data=task_data, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Created task: {task_data['content']}")
                # After creating a task, we need to fetch and update the task_ids
                self.task_ids = self.get_task_ids()  # Update task_ids list
            else:
                response.failure("Failed to create task")

    @task
    def delete_task(self):
        """
            Simulates task deletion by sending a GET request to the /delete/<task_id> route.

            This method deletes a task with a random ID from the list of available task IDs.
            - If there are no tasks to delete (i.e., the task list is empty), it creates a task first by calling the `create_task()` method.
            - Once tasks are available, it randomly selects a task and sends a DELETE request to remove the task.
            - The task ID is removed from the local task list after a successful deletion.

            Args:
                None.

            Returns:
                None. If task deletion is successful, the task ID is removed from the list. If it fails, an appropriate error message is logged.
        """
        if not self.task_ids:  # Check if there are any tasks to delete
            print("No tasks available to delete, creating a task first...")
            self.create_task()  # Create a task to ensure task_ids is populated
            self.task_ids = self.get_task_ids()  # Refresh task_ids after creating a task

        if self.task_ids:  # Proceed if task_ids is now populated
            task_id = random.choice(self.task_ids)
            with self.client.get(f"/delete/{task_id}", catch_response=True) as response:
                if response.status_code == 302:  # Handle redirect after successful delete
                    self.task_ids.remove(task_id)  # Remove deleted ID from local list
                    response.success()
                elif response.status_code == 200 and "There was a problem" in response.text:
                    response.failure("Failed to delete task")
                else:
                    response.failure(f"Unexpected response: {response.status_code}")
