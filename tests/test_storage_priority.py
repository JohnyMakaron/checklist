import unittest

from src.storage import load_tasks


class StoragePriorityCompatibilityTests(unittest.TestCase):
    def test_load_tasks_defaults_missing_priority_to_medium(self):
        tasks = load_tasks()
        self.assertTrue(tasks)
        for task in tasks:
            self.assertIn("priority", task)
            self.assertEqual(task["priority"], "medium")


if __name__ == "__main__":
    unittest.main()
