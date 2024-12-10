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
        """Simulate a login to the app."""
        # Perform OAuth login
        login_data = self.login()
        if login_data['status'] == 'ok':
            self.user_id = login_data['user_id']  # Store user_id after login
            self.task_ids = self.get_task_ids()  # Populate task_ids list after login
        else:
            raise StopUser("Login failed, stopping user")

    def login(self):
        """Perform OAuth login by simulating a GET request to the /oauth-login route"""
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
        """Fetch task IDs by parsing the HTML response"""
        with self.client.get("/index", catch_response=True) as response:
            if response.status_code == 200:
                # Use regex to find task IDs in the HTML table
                task_ids = re.findall(r'/delete/(\d+)', response.text)
                return [int(task_id) for task_id in task_ids]  # Convert IDs to integers
            response.failure("Failed to load task IDs")
            return []

    @task
    def create_task(self):
        """Simulate task creation"""
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
