from typing import Any, Dict, Type

from django.contrib import admin
from django.db import models


class CollaborativeAdminMixin:
    """
    Mixin for ModelAdmin classes to enable collaborative editing.

    This mixin adds the necessary JavaScript to the admin interface
    for real-time collaboration features.
    """

    class Media:
        js = ('django_admin_collaborator/js/admin_edit.js',)


def make_collaborative(admin_class: Type[admin.ModelAdmin]) -> Type[admin.ModelAdmin]:
    """
    Function to dynamically add collaborative editing to an existing ModelAdmin class.

    Args:
        admin_class: The ModelAdmin class to enhance

    Returns:
        A new ModelAdmin class with collaborative editing capabilities
    """

    class CollaborativeAdmin(CollaborativeAdminMixin, admin_class):
        pass

    return CollaborativeAdmin


def collaborative_admin_factory(model_class: Type[models.Model],
                                admin_options: Dict[str, Any] = None,
                                base_admin_class: Type[admin.ModelAdmin] = admin.ModelAdmin) -> Type[admin.ModelAdmin]:
    """
    Factory function to create a collaborative ModelAdmin for a model.

    Args:
        model_class: The model class for which to create the admin
        admin_options: Optional dictionary of admin options
        base_admin_class: Base admin class to extend from (default: admin.ModelAdmin)

    Returns:
        A ModelAdmin class with collaborative editing capabilities
    """
    if admin_options is None:
        admin_options = {}

    # Create a new class dynamically
    attrs = {**admin_options}

    # Create the base admin class
    AdminClass = type(
        f'Collaborative{model_class.__name__}Admin',
        (base_admin_class,),
        attrs
    )

    # Add collaborative functionality
    return make_collaborative(AdminClass)