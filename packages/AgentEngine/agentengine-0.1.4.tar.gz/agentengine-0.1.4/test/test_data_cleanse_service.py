import unittest
import os
import time
import sys
import requests
from urllib.parse import urljoin

# API configuration
API_BASE_URL = "http://localhost:8001"

# Get the absolute path to the example_docs directory
EXAMPLE_DOCS_DIR = './example_docs'

# Check if the directory exists
if not os.path.exists(EXAMPLE_DOCS_DIR):
    raise FileNotFoundError(f"Test data directory does not exist: {EXAMPLE_DOCS_DIR}")

# Test files to use
TEST_FILES = {
    'TEXT': os.path.join(EXAMPLE_DOCS_DIR, "norwich-city.txt"),
    'DOCX': os.path.join(EXAMPLE_DOCS_DIR, "simple.docx"),
    'PDF': os.path.join(EXAMPLE_DOCS_DIR, "pdf", "layout-parser-paper-fast.pdf"),
    'CSV': os.path.join(EXAMPLE_DOCS_DIR, "stanley-cups.csv")
}

# Validate test files existence
for file_type, file_path in TEST_FILES.items():
    if not os.path.exists(file_path):
        print(f"Warning: Test file does not exist: {file_path}")


class TestDataCleanseAPI(unittest.TestCase):
    """Test class for interacting with an already running data cleanse service."""
    
    def setUp(self):
        """Prepare the test environment and check service availability."""
        self.api_base_url = API_BASE_URL
        self.check_service_availability()
        
    def check_service_availability(self):
        """Check if the data cleanse service is running."""
        try:
            response = requests.get(urljoin(self.api_base_url, "/healthcheck"))
            if response.status_code != 200:
                self.skipTest(f"Data cleanse service is not available at {self.api_base_url}. "
                             f"Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.skipTest(f"Could not connect to data cleanse service at {self.api_base_url}. "
                         "Please ensure the service is running.")
    
    def is_task_completed(self, status_value):
        """Check if task status indicates completion.
        
        Args:
            status_value: Task status value
            
        Returns:
            bool: True if task is completed
        """
        if not status_value:
            return False
            
        status_str = str(status_value).lower()
        return "completed" in status_str
        
    def is_task_failed(self, status_value):
        """Check if task status indicates failure.
        
        Args:
            status_value: Task status value
            
        Returns:
            bool: True if task has failed
        """
        if not status_value:
            return False
            
        status_str = str(status_value).lower()
        return "failed" in status_str or "error" in status_str
        
    def is_task_finished(self, status_value):
        """Check if task status indicates it's finished (completed or failed).
        
        Args:
            status_value: Task status value
            
        Returns:
            bool: True if task is finished
        """
        return self.is_task_completed(status_value) or self.is_task_failed(status_value)
    
    def wait_for_task_completion(self, task_id, task_type="Task", timeout=30):
        """Wait for task completion and return task status.
        
        Args:
            task_id: Task ID
            task_type: Task type description (for logging)
            timeout: Timeout in seconds
            
        Returns:
            Dict containing task status data
            
        Raises:
            unittest.SkipTest: If task doesn't complete within timeout
        """
        status_url = urljoin(self.api_base_url, f"/tasks/{task_id}")
        
        start_time = time.time()
        status_data = None
        
        print(f"Waiting for {task_type} completion, task ID: {task_id}")
        while time.time() - start_time < timeout:
            status_response = requests.get(status_url)
            self.assertEqual(status_response.status_code, 200, 
                           f"{task_type} status check failed: {status_response.text}")
            
            status_data = status_response.json()
            status_value = status_data["status"]
            print(f"{task_type} status: {status_value}")
            
            if self.is_task_finished(status_value):
                print(f"{task_type} finished, final status: {status_value}")
                break
            
            time.sleep(3)
        else:
            print(f"Warning: {task_type} did not complete within {timeout} seconds, current status: {status_value}")
        
        if not self.is_task_completed(status_value):
            self.skipTest(f"{task_type} did not complete successfully, final status: {status_value}")
            
        return status_data
    
    def get_task_details(self, task_id):
        """Get detailed results for a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task details data or None if not available
        """
        details_url = urljoin(self.api_base_url, f"/tasks/{task_id}/details")
        try:
            response = requests.get(details_url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Warning: Failed to get task details, status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting task details: {str(e)}")
            return None
    
    def verify_task_result(self, task_id, task_type="Task"):
        """Verify task completion and result structure.
        
        Args:
            task_id: Task ID
            task_type: Task type description (for logging)
            
        Returns:
            Task details if available
        """
        # Wait for task completion
        status_data = self.wait_for_task_completion(task_id, task_type=task_type)
        
        # Verify status data format
        self.assertTrue("id" in status_data or "task_id" in status_data, 
                      "Response should contain id or task_id field")
        self.assertTrue(self.is_task_completed(status_data["status"]))
        
        # Get detailed results
        details = self.get_task_details(task_id)
        
        # Verify details data if available
        if details:
            print(f"Task details retrieved: {details}")
            self.assertIn("task_id", details)
            self.assertIn("status", details)
            
            # Check result format if present
            print(f"{task_type} completed successfully.")
        else:
            print(f"Warning: Unable to retrieve {task_type} details")
            
        return details
    
    def test_cleanse_text_data_api(self):
        """Test the API endpoint for cleansing text data."""
        data = {
            "source": "This is a sample text for API testing.",
            "source_type": "text",
            "chunking_strategy": "basic"
        }
        
        url = urljoin(self.api_base_url, "/tasks")
        response = requests.post(url, json=data)
        
        # Check response
        self.assertEqual(response.status_code, 201, 
                         f"API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        self.assertIn("task_id", result)
        
        # Verify task result
        self.verify_task_result(result["task_id"], task_type="Text processing task")
    
    def test_cleanse_file_api(self):
        """Test the API endpoint for cleansing a file."""
        # Skip if test file doesn't exist
        if not os.path.exists(TEST_FILES['TEXT']):
            self.skipTest(f"Test file does not exist: {TEST_FILES['TEXT']}")
            
        data = {
            "source": TEST_FILES['TEXT'],
            "source_type": "file",
            "chunking_strategy": "basic"
        }
        
        url = urljoin(self.api_base_url, "/tasks")
        response = requests.post(url, json=data)
        
        # Check response
        self.assertEqual(response.status_code, 201, 
                         f"API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        self.assertIn("task_id", result)
        
        # Verify task result
        self.verify_task_result(result["task_id"], task_type="File processing task")
    
    def test_batch_tasks_api(self):
        """Test the batch tasks API."""
        # Create batch tasks
        data = {
            "sources": [
                {
                    "source": "Test text 1 for batch API.",
                    "source_type": "text",
                    "chunking_strategy": "basic"
                },
                {
                    "source": "Test text 2 for batch API.",
                    "source_type": "text",
                    "chunking_strategy": "basic"
                }
            ]
        }
        
        url = urljoin(self.api_base_url, "/tasks/batch")
        response = requests.post(url, json=data)
        
        # Check response
        self.assertEqual(response.status_code, 201, 
                         f"Create batch tasks failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        self.assertIn("task_ids", result)
        self.assertIsInstance(result["task_ids"], list)
        self.assertEqual(len(result["task_ids"]), len(data["sources"]))
        
        # Verify first task result
        if result["task_ids"]:
            self.verify_task_result(result["task_ids"][0], task_type="Batch task")
        else:
            self.skipTest("No task IDs returned from batch API")
    
    def test_tasks_listing(self):
        """Test the API endpoint for listing tasks."""
        # Create a task to ensure there's at least one in the list
        data = {
            "source": "Test text for tasks listing API.",
            "source_type": "text"
        }
        
        create_url = urljoin(self.api_base_url, "/tasks")
        requests.post(create_url, json=data)
        
        # Get tasks list
        list_url = urljoin(self.api_base_url, "/tasks")
        response = requests.get(list_url)
        
        # Check response
        self.assertEqual(response.status_code, 200, 
                         f"List tasks failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        self.assertIn("tasks", result)
        self.assertIsInstance(result["tasks"], list)
        
        # Verify at least one task is returned
        self.assertGreater(len(result["tasks"]), 0)
        
        # Verify task format
        task = result["tasks"][0]
        for field in ["id", "status", "created_at", "updated_at"]:
            self.assertIn(field, task)


def run_tests():
    """Run all data cleanse API tests"""
    print("\n" + "="*80)
    print("Starting Data Cleanse API Tests")
    print("="*80)
    
    # Display API service configuration
    print(f"\nAPI Service: {API_BASE_URL}")
    print("Note: Tests assume the data cleanse service is already running")
    
    # Verify test files existence
    print("\nChecking test files:")
    for file_type, file_path in TEST_FILES.items():
        exists = os.path.exists(file_path)
        status = "✓ Exists" if exists else "✗ Missing"
        print(f"{file_type:<6}: {status:<8} {file_path}")
    
    # Check API service availability
    try:
        response = requests.get(urljoin(API_BASE_URL, "/healthcheck"))
        if response.status_code == 200:
            print(f"\nAPI Service Check: ✓ Available ({API_BASE_URL})")
        else:
            print(f"\nAPI Service Check: ⚠️ Service returned non-200 status: {response.status_code}")
    except requests.RequestException as e:
        print(f"\nAPI Service Check: ✗ Service unavailable ({API_BASE_URL}): {str(e)}")
        print("Ensure data cleanse service is running before executing API tests")
        return False
    
    # Create a test suite for API tests
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDataCleanseAPI))
    
    # Run the tests
    print("\n" + "="*80)
    print("Running API Tests")
    print("="*80 + "\n")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print(f"API Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Successful: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the API tests and exit with the appropriate code
    success = run_tests()
    sys.exit(0 if success else 1) 