from django.contrib import admin

from .models import Service, Team


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    sortable_by = ()
    list_display = ('name', 'description', 'is_active')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    sortable_by = ()
    list_display = ('service', 'leader', 'get_members_qty')
    fields = ('service', 'leader', 'members')
    readonly_fields = ('service', 'get_members_qty')
    filter_horizontal = ('members',)
    # form = TeamForm

    @admin.display(description='membros')
    def get_members_qty(self, obj):
        return len(obj.members.all())

    def has_add_permission(self, request):
        return False

    # Hide delete button instead of revoke delete permission
    # because the Team must be deleted when the service is deleted
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url=form_url, extra_context=dict(show_delete=False))
