"""Unit tests for TaskStore service."""

import unittest
from datetime import datetime, timedelta
from src.models.task import Task
from src.models.enums import Status, Priority
from src.services.task_store import TaskStore
from src.models.recurrence_rule import RecurrenceRule, RecurrenceType


class TestTaskStore(unittest.TestCase):
    """Test TaskStore in-memory storage operations."""

    def setUp(self):
        """Set up fresh TaskStore for each test."""
        self.store = TaskStore()

    def test_add_task_assigns_id(self):
        """Test add assigns auto-incrementing ID starting at 1."""
        task = Task(
            id=0,  # ID should be overwritten
            title="Task 1"
        )

        added_task = self.store.add(task)

        self.assertEqual(added_task.id, 1)

    def test_add_task_stores_task(self):
        """Test add stores task in storage."""
        task = Task(
            id=0,
            title="Task 1"
        )

        added_task = self.store.add(task)
        retrieved_task = self.store.get(added_task.id)

        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "Task 1")

    def test_add_multiple_tasks_increments_id(self):
        """Test multiple adds increment ID sequentially."""
        task1 = self.store.add(Task(id=0, title="Task 1"))
        task2 = self.store.add(Task(id=0, title="Task 2"))
        task3 = self.store.add(Task(id=0, title="Task 3"))

        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_get_existing_task(self):
        """Test get returns task for existing ID."""
        task = Task(
            id=0,
            title="Task 1"
        )

        added_task = self.store.add(task)
        retrieved_task = self.store.get(added_task.id)

        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, added_task.id)
        self.assertEqual(retrieved_task.title, "Task 1")

    def test_get_nonexistent_task(self):
        """Test get returns None for nonexistent ID."""
        task = self.store.get(999)

        self.assertIsNone(task)

    def test_delete_existing_task(self):
        """Test delete removes task and returns True."""
        task = self.store.add(Task(id=0, title="Task 1"))

        result = self.store.delete(task.id)
        retrieved_task = self.store.get(task.id)

        self.assertTrue(result)
        self.assertIsNone(retrieved_task)

    def test_delete_nonexistent_task(self):
        """Test delete returns False for nonexistent ID."""
        result = self.store.delete(999)

        self.assertFalse(result)

    def test_update_existing_task(self):
        """Test update modifies task fields."""
        task = self.store.add(Task(id=0, title="Task 1"))

        updated_task = self.store.update(task.id, title="Updated task")

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated task")
        self.assertIsNotNone(updated_task.updated_at)

    def test_update_nonexistent_task(self):
        """Test update returns None for nonexistent ID."""
        updated_task = self.store.update(999, title="Updated")

        self.assertIsNone(updated_task)

    def test_list_all_empty(self):
        """Test list_all returns empty list when no tasks."""
        tasks = self.store.list_all()

        self.assertEqual(tasks, [])

    def test_list_all_with_tasks(self):
        """Test list_all returns all tasks."""
        task1 = self.store.add(Task(id=0, title="Task 1"))
        task2 = self.store.add(Task(id=0, title="Task 2"))

        tasks = self.store.list_all()

        self.assertEqual(len(tasks), 2)

    def test_exists_existing_task(self):
        """Test exists returns True for existing task."""
        task = self.store.add(Task(id=0, title="Task 1"))

        self.assertTrue(self.store.exists(task.id))

    def test_exists_nonexistent_task(self):
        """Test exists returns False for nonexistent task."""
        self.assertFalse(self.store.exists(999))

    def test_count_empty(self):
        """Test count returns 0 for empty store."""
        self.assertEqual(self.store.count(), 0)

    def test_count_with_tasks(self):
        """Test count returns correct task count."""
        self.store.add(Task(id=0, title="Task 1"))
        self.store.add(Task(id=0, title="Task 2"))
        self.store.add(Task(id=0, title="Task 3"))

        self.assertEqual(self.store.count(), 3)


if __name__ == "__main__":
    unittest.main()
