"""Tests for Django Admin Collaborator consumers."""

import json
from unittest.mock import patch, MagicMock

from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from django_admin_collaborator.consumers import AdminEditConsumer

User = get_user_model()


class MockRedis:
    """Mock Redis client for testing."""

    def __init__(self):
        self.data = {}

    def exists(self, key):
        return key in self.data

    def get(self, key):
        if key in self.data:
            return self.data[key].encode('utf-8')
        return None

    def set(self, key, value):
        self.data[key] = value

    def setex(self, key, expire, value):
        # Ignore expiration in tests
        self.data[key] = value

    def delete(self, key):
        if key in self.data:
            del self.data[key]


class AdminEditConsumerTests(TestCase):
    """Test the AdminEditConsumer."""

    async def test_connect(self):
        """Test connection to the consumer."""
        user = await self._create_user()

        # Create a communicator
        communicator = WebsocketCommunicator(
            AdminEditConsumer.as_asgi(),
            "/admin-edit-consumer/app/model/1/"
        )

        # Mock authentication and Redis
        communicator.scope["user"] = user
        communicator.scope["url_route"] = {
            "kwargs": {
                "app_label": "app",
                "model_name": "model",
                "object_id": "1"
            }
        }

        with patch('django_admin_collaborator.consumers.AdminEditConsumer.redis_client',
                   MagicMock(return_value=MockRedis())):
            # Connect
            connected, _ = await communicator.connect()

            # Check that we got a connection
            self.assertTrue(connected)

            # Receive the user_joined message
            response = await communicator.receive_json_from()
            self.assertEqual(response["type"], "user_joined")

            # Close
            await communicator.disconnect()

    @staticmethod
    async def _create_user():
        """Create a test user."""
        return await sync_to_async(User.objects.create_user)(
            username="testuser",
            email="test@example.com",
            password="password123",
            is_staff=True
        )


# Helper function to run synchronous functions in async context
from asgiref.sync import sync_to_async