from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django_todo.apps.core.models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='test_user', email='test@email.com', password='secret')
        Task.objects.create(
            description='Beautiful is better than ugly',
            is_checked=False,
            user=self.user)
        Task.objects.create(
            description='Simple is better than complex',
            is_checked=True,
            user=self.user,
            date_done=datetime.now())
        Task.objects.create(
            description='Explicit is better than implicit',
            is_checked=False,
            user=self.user)

    def test_pending_tasks_are_not_retrieved(self):
        """Pending tasks filter must not recover completed tasks."""
        tasks = Task.objects.pending_tasks(self.user)
        self.assertGreater(len(tasks), 0)
        self.assertEqual(tasks[0].is_checked, False)

    def test_pending_tasks_are_retrieved_in_order(self):
        """Newest tasks must be on top."""
        tasks = Task.objects.pending_tasks(self.user)
        self.assertNotEqual(len(tasks), 0)
        self.assertEqual(tasks[0].is_checked, False)
        # The last created task is the newest
        self.assertEqual(tasks[0].description, 'Explicit is better than implicit')
