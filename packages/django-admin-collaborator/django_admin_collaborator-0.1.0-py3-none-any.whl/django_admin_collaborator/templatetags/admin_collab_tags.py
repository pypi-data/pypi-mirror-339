"""Template tags for Django Admin Collaborator."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def admin_collaborator_status_banner():
    """
    Render a banner to show collaborative editing status.

    Returns:
        HTML for the status banner
    """
    html = """
    <div id="admin-collaborator-status" 
         style="display: none; background-color: #f8f9fa; padding: 10px; margin-bottom: 10px; border-radius: 4px;">
        <div id="admin-collaborator-status-message"></div>
    </div>
    """
    return mark_safe(html)


@register.simple_tag
def admin_collaborator_scripts():
    """
    Include the necessary JavaScript for admin collaboration.

    This tag can be used in custom admin templates to include the scripts
    in a specific location.

    Returns:
        HTML script tag for the admin_edit.js file
    """
    return mark_safe(
        '<script src="/static/django_admin_collaborator/js/admin_edit.js"></script>'
    )