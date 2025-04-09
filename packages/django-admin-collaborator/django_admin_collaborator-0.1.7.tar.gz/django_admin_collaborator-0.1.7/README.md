# Django Admin Collaborator

Real-time collaborative editing for Django admin interfaces using WebSockets.

## Overview
![Demo](https://raw.githubusercontent.com/Brktrlw/django-admin-collaborator/refs/heads/main/screenshots/demo.gif)

## Features

- Real-time presence indicators - see who else is viewing the same object
- Exclusive editing mode - prevents conflicts by allowing only one user to edit at a time
- Automatic lock release - abandoned sessions automatically release editing privileges
- Seamless integration with Django admin - minimal configuration required
- User avatars and status indicators - visual feedback on who's editing
- Automatic page refresh when content changes - stay up to date without manual refreshes

## Requirements

- Django 3.2+
- Redis (for lock management and message distribution)
- Channels 3.0+

## Installation

```bash
pip install django-admin-collaborator
```

## Quick Start

1. Add to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ...
    'channels',
    'django_admin_collaborator',
    # ...
]
```

2. Set up Redis in your settings:

```python
# Optional: Configure Redis connection (defaults to localhost:6379/0)
ADMIN_COLLABORATOR_REDIS_URL = 'redis://localhost:6379/0'

# Or use the same Redis URL you have for Channels if you're already using it
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
}
```

3. Set up the ASGI application:

```python
# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

django_asgi_app = get_asgi_application()
from django_admin_collaborator.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
```

4. Enable collaborative editing for specific admin classes:

```python
from django.contrib import admin
from django_admin_collaborator.utils import CollaborativeAdminMixin
from myapp.models import MyModel

@admin.register(MyModel)
class MyModelAdmin(CollaborativeAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description')
    # ... your other admin configurations
```

5. Run your project using an ASGI server like Daphne or Uvicorn:

```bash
daphne yourproject.asgi:application
# OR
uvicorn yourproject.asgi:application --host 0.0.0.0 --reload --reload-include '*.html'
```

## Advanced Usage

### Applying to Multiple Admin Classes

You can use the utility functions to apply collaborative editing to existing admin classes:

```python
from django.contrib import admin
from django_admin_collaborator.utils import make_collaborative
from myapp.models import MyModel

# Create your admin class
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    # ... your other admin configurations

# Apply collaborative editing
CollaborativeMyModelAdmin = make_collaborative(MyModelAdmin)

# Register with admin
admin.site.register(MyModel, CollaborativeMyModelAdmin)
```

### Creating Admin Classes Dynamically

You can use the factory function to create admin classes dynamically:

```python
from django.contrib import admin
from django_admin_collaborator.utils import collaborative_admin_factory
from myapp.models import MyModel

# Create and register the admin class in one go
admin.site.register(
    MyModel, 
    collaborative_admin_factory(
        MyModel, 
        admin_options={
            'list_display': ('name', 'description'),
            'search_fields': ('name',),
        }
    )
)
```

## Deployment on Heroku
If you're deploying this application on Heroku, ensure that you configure the database connection settings appropriately to optimize performance. Specifically, Heroku may require you to set the `CONN_MAX_AGE` to 0 to avoid persistent database connections.
Add the following to your settings.py file:
```python
if not DEBUG:
    import django_heroku
    django_heroku.settings(locals())
    DATABASES['default']['CONN_MAX_AGE'] = 0
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.