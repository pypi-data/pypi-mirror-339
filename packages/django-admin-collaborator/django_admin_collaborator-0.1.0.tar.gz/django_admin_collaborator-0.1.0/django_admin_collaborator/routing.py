from django.urls import path

from django_admin_collaborator.consumers import AdminEditConsumer

websocket_urlpatterns = [
    path('admin-edit-consumer/<str:app_label>/<str:model_name>/<str:object_id>/',
         AdminEditConsumer.as_asgi()),
]