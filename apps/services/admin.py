from django.contrib import admin
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from apps.accounts.models import Member

from .models import Project, Request, RequestDiscussion, Task


class RequestDiscussionInline(admin.StackedInline):
    model = RequestDiscussion
    template = 'admin/services/request/edit_inline/stacked.html'
    verbose_name_plural = 'Discussão da solicitação'
    exclude = ('author', 'created_at')
    extra = 1


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    sortable_by = ()
    list_display = ('get_business_name', 'service', 'status', 'has_project')
    list_filter = ('status',)
    fields = (
        'client',
        'get_business_name',
        'service',
        'description',
        'attachment',
        'preferred_method_of_contact',
        'get_preferred_contact',
        'best_time_to_contact',
        'status',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('get_business_name', 'get_preferred_contact', 'created_at', 'updated_at')
    # inlines = (RequestDiscussionInline,)

    @admin.display(description='negócio')
    def get_business_name(self, obj):
        return obj.client.business.name

    @admin.display(description='contato de preferência')
    def get_preferred_contact(self, obj):
        if obj.preferred_method_of_contact == Request.PREFER_EMAIL:
            return obj.client.email
        return obj.client.business.telephone

    @admin.display(description='possui projeto', boolean=True)
    def has_project(self, obj):
        return bool(Project.objects.filter(request=obj).first())

    def get_fields(self, request, obj=None):
        if obj is None:
            return (
                'client',
                'service',
                'description',
                'attachment',
                'preferred_method_of_contact',
                'best_time_to_contact',
                'status',
            )
        return super().get_fields(request, obj=obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        member = Member.objects.get(pk=request.user.pk)
        if str(request.user.profile.member_type) != 'Coordenador':
            return qs.filter(
                Q(service__in=member.teams_led.values_list('service')) |
                Q(service__in=member.teams.values_list('service'))
            )
        return qs

    def get_inlines(self, request, obj=None):
        if not obj:
            return ()
        return super().get_inlines(request, obj=obj)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('create-project/', self.create_project),
        ]
        return my_urls + urls

    def create_project(self, request):
        body = request.body.decode()
        request_pk = body.split('request=')[1:][0]
        request_instance = Request.objects.get(pk=request_pk)
        project = Project.objects.create(request=request_instance)
        project_reverse_url = reverse('admin:services_project_change', args=(project.pk,))
        self.message_user(request, format_html(f'O projeto “<a href="{project_reverse_url}">{project}</a>” foi adicionado com sucesso. Você pode editá-lo novamente abaixo.'))
        return HttpResponseRedirect(project_reverse_url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        project = Project.objects.filter(request=object_id)
        extra_context['has_project'] = bool(project)
        if extra_context['has_project']:
            extra_context['project'] = project[0]
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def save_formset(self, request, form, formset, change):
        """Grava o usuário logado no campo author do ProjectDiscussionInline
        quando uma nova postagem é feita na discussão do projeto
        """
        for form in formset.forms:
            if not form.instance.pk:
                form.instance.author = request.user
        return super().save_formset(request, form, formset, change)


class TaskInline(admin.StackedInline):
    model = Task
    exclude = ('author', 'created_at',)
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    sortable_by = ()
    list_display = ('request', 'created_at')
    fields = (
        'request',
        'theme',
        'general_objective',
        'specific_objectives',
        'justification',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('request', 'created_at', 'updated_at')
    inlines = (TaskInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            member = Member.objects.get(pk=request.user.pk)
            user_is_leader = Project.objects.filter(request__service__in=member.teams_led.values_list('service'))
            if user_is_leader:
                return super().get_readonly_fields(request, obj=obj)
        return self.fields

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        member = Member.objects.get(pk=request.user.pk)
        if str(request.user.profile.member_type) != 'Coordenador':
            return qs.filter(
                Q(request__service__in=member.teams_led.values_list('service')) |
                Q(request__service__in=member.teams.values_list('service'))
            )
        return qs

    def save_formset(self, request, form, formset, change):
        """Grava o usuário logado no campo author do TaskInline
        quando uma nova tarefa é atribuída ao projeto
        """
        for form in formset.forms:
            if not form.instance.pk:
                form.instance.author = request.user
        return super().save_formset(request, form, formset, change)
