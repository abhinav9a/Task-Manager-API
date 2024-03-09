from django.contrib import admin
from api.models import Task

class TaskAdmin(admin.ModelAdmin):
  list_display = ['title', 'description', 'completed', 'created_at', 'updated_at']
  readonly_fields = ['created_at', 'updated_at']
  list_filter = ['completed']


admin.site.register(Task, TaskAdmin)