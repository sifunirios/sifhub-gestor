from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('gestor/', admin.site.urls),
]

# Admin Site
admin.site.site_title = 'SifHub Gestor'
admin.site.site_header = 'SifHub Gestor'
admin.site.index_title = 'Dashboard'

admin.site.disable_action('delete_selected')
