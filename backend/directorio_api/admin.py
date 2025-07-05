# backend/directorio_api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User, Category, Provider, Rating, Comment

class CustomUserAdmin(UserAdmin):
   """
   Personaliza la vista del modelo User en el admin.
   """
   model = User
   # Campos a mostrar en la lista de usuarios
   list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
   # Filtros para facilitar la búsqueda
   list_filter = ['is_active', 'is_staff', 'groups']
   # Campos en los que se puede buscar
   search_fields = ['username', 'first_name', 'last_name', 'email']
   # Permite editar estos campos directamente desde la lista
   list_editable = ['is_active']

# Se añade 'phone_number' a los formularios de creación y edición
fieldsets = UserAdmin.fieldsets + (
   (None, {'fields': ('phone_number',)}),
    )
add_fieldsets = UserAdmin.add_fieldsets + (
   (None, {'fields': ('phone_number',)}),
   )

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
   list_display = ('name', 'category', 'location', 'phone', 'submitted_by', 'created_at')
   list_filter = ('category', 'location')
   search_fields = ('name', 'phone')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
   list_display = ('provider', 'user', 'created_at', 'is_visible')
   list_filter = ('is_visible', 'created_at')
   search_fields = ('body', 'user__username', 'provider__name')
   list_editable = ['is_visible'] # Permite moderar comentarios rápidamente

# Registrar los modelos en el sitio de administración
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Rating) # Se registra para consulta, pero no suele editarse manualmente