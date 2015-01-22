from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_todo.apps.core.models import Task


def create_tasks(user):
    Task.objects.create(
        description='Beautiful is better than ugly',
        is_checked=False,
        user=user)
    Task.objects.create(
        description='Simple is better than complex',
        is_checked=True,
        user=user,
        date_done=datetime.now())
    Task.objects.create(
        description='Explicit is better than implicit',
        is_checked=False,
        user=user)


class TaskTestCase(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='test_user', email='test@email.com', password='secret')
        create_tasks(self.user)

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


class CurrentTaskViewTests(TestCase):
    def setUp(self):
        self.password = 'secret'
        self.user = User.objects.create_user(username='test_user', email='test@email.com', password=self.password)

    def test_home_without_user_logged_in(self):
        """If no user is logged, then redirect to login page."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_home_with_user_logged_in_and_no_tasks(self):
        """If user is logged, then retrieve the pending tasks."""
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['tasks'], [])

    def test_home_with_user_logged_in(self):
        """If user is logged, then retrieve the pending tasks."""
        self.client.login(username=self.user.username, password=self.password)
        create_tasks(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

    def test_add_new_task(self):
        """If user is logged, and form is valid, then save a new task."""
        description = 'Readability counts.'
        self.client.login(username=self.user.username, password=self.password)
        create_tasks(self.user)
        # check that the task does not exists
        self.assertFalse(Task.objects.filter(description=description).exists())
        response = self.client.post(reverse('create_task'), data={'description': description})
        self.assertEqual(response.status_code, 302)  # We got 302 because there is a redirect.
        # check that the task does exists
        self.assertTrue(Task.objects.filter(description=description).exists())

    def test_complete_task(self):
        """If user is logged, and form is valid, then mark task as completed."""
        self.client.login(username=self.user.username, password=self.password)
        create_tasks(self.user)
        task_id = Task.objects.all()[0].id
        self.assertTrue(Task.objects.filter(pk=task_id).exists())
        response = self.client.post(reverse('complete_task', kwargs={'id': task_id}))
        self.assertEqual(response.status_code, 302)  # We got 302 because there is a redirect.
        self.assertTrue(Task.objects.get(pk=task_id).is_checked)
