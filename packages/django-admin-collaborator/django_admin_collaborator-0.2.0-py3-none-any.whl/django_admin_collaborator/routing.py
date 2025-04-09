from django.urls import path

from django_admin_collaborator.consumers import AdminCollaborationConsumer

websocket_urlpatterns = [
    path('admin/collaboration/<str:app_label>/<str:model_name>/<str:object_id>/',
         AdminCollaborationConsumer.as_asgi()),
]