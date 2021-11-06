from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import ClientBusinessForm, MemberProfileForm
from .models import Client, ClientBusiness, Member, MemberProfile


class ClientBusinessInline(admin.StackedInline):
    model = ClientBusiness
    template = 'admin/accounts/edit_inline/stacked.html'
    verbose_name_plural = 'Negócio'
    form = ClientBusinessForm
    can_delete = False


@admin.register(Client)
class ClientAdmin(BaseUserAdmin):
    search_fields = ('email', 'name', 'surname', 'business__name')
    sortable_by = ()
    list_display = ('email', 'get_full_name', 'get_business_name', 'get_branch_of_activity')
    ordering = ('name', 'surname')
    list_filter = ('is_active',)
    filter_horizontal = ()
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname'),
        }),
    )
    fieldsets = (
        ('Autenticação', {'fields': ('email', 'password', 'is_active')}),
        ('Informações pessoais', {'fields': ('name', 'surname', 'photo')}),
        ('Datas importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    inlines = (ClientBusinessInline,)

    @admin.display(description='negócio')
    def get_business_name(self, obj):
        return obj.business.name or '-'

    @admin.display(description='ramo de atividade')
    def get_branch_of_activity(self, obj):
        return obj.business.get_branch_of_activity_display()

    class Media:
        js = (
            'js/vendor/jquery.mask.min.js',
            'admin/js/masks.js',
        )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return ()
        return super().get_inline_instances(request, obj=obj)


class MemberProfileInline(admin.StackedInline):
    model = MemberProfile
    template = 'admin/accounts/edit_inline/stacked.html'
    verbose_name_plural = 'Perfil'
    form = MemberProfileForm
    can_delete = False


@admin.register(Member)
class MemberAdmin(BaseUserAdmin):
    search_fields = ('email', 'name', 'surname', 'registry')
    sortable_by = ()
    list_display = ('email', 'get_full_name', 'get_member_type')
    ordering = ('name', 'surname')
    list_filter = ('is_active', 'profile__member_type')
    filter_horizontal = ('user_permissions',)
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname'),
        }),
    )
    fieldsets = (
        ('Autenticação e Autorização', {
            'fields': ('email', 'password', 'is_active', 'is_superuser', 'user_permissions'),
        }),
        ('Informações pessoais', {'fields': ('name', 'surname', 'photo')}),
        ('Datas importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    inlines = (MemberProfileInline,)

    @admin.display(description='tipo')
    def get_member_type(self, obj):
        return obj.profile.member_type

    class Media:
        js = (
            'js/vendor/jquery.mask.min.js',
            'admin/js/masks.js',
        )

    def get_readonly_fields(self, request, obj):
        extra_readonly = []
        if not request.user.is_superuser:
            extra_readonly.append('is_superuser')
        if request.user == obj:
            extra_readonly.append('is_active')
            if request.user.is_superuser:
                extra_readonly.append('is_superuser')
        return self.readonly_fields + tuple(extra_readonly)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return ()
        return super().get_inline_instances(request, obj=obj)


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    fields = ('permissions',)

    def has_add_permission(self, request):
        return False
