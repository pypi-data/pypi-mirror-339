from sqladmin import ModelView
from .models import {{ app_class_name }}
from app.core.main_admin import register_admin

@register_admin
class {{ app_class_name }}Admin(ModelView, model={{ app_class_name }}):
    column_list = [{{ app_class_name }}.id, {{ app_class_name }}.name, {{ app_class_name }}.created_at]
    column_searchable_list = [{{ app_class_name }}.name]
    column_sortable_list = [{{ app_class_name }}.name, {{ app_class_name }}.created_at]
    column_filters = [{{ app_class_name }}.name, {{ app_class_name }}.created_at]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
