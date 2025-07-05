# backend/directorio_api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg, Count

class User(AbstractUser):
    """
    Modelo de Usuario personalizado.
    Hereda de AbstractUser de Django para incluir todos los campos de autenticación
    y se extiende con los campos solicitados.
    """
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Número de celular")
    
    # El campo 'is_active' de Django se usará para la validación del administrador.
    # Por defecto, un usuario creado no estará activo hasta que el admin lo valide.
    # 'is_staff' e 'is_superuser' se usarán para el rol de administrador.

    def __str__(self):
        return self.get_full_name() or self.username

class Category(models.Model):
    """
    Modelo para las categorías de servicios (ej. Plomería, Electricidad).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la categoría")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name

class Provider(models.Model):
    """
    Modelo para los proveedores de servicios.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre o Razón Social")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    location = models.CharField(max_length=100, verbose_name="Población")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='providers', verbose_name="Categoría")
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_providers', verbose_name="Registrado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de alta")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def global_rating(self):
        """
        Calcula la calificación global promedio de todas las calificaciones recibidas.
        Devuelve 0 si no hay calificaciones.
        """
        average = self.ratings.aggregate(Avg('total_score'))['total_score__avg']
        return round(average, 2) if average is not None else 0.0

    @property
    def rating_count(self):
        """
        Cuenta cuántos usuarios han calificado a este proveedor.
        """
        return self.ratings.count()

class Rating(models.Model):
    """
    Modelo para almacenar la calificación que un usuario da a un proveedor.
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='ratings', verbose_name="Proveedor")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name="Usuario")
    
    # Puntuaciones para cada criterio, basadas en la matriz.
    quality_score = models.FloatField(verbose_name="Puntuación de Calidad")
    price_score = models.FloatField(verbose_name="Puntuación de Precio")
    communication_score = models.FloatField(verbose_name="Puntuación de Comunicación")
    deadline_score = models.FloatField(verbose_name="Puntuación de Cumplimiento")
    
    # Puntuación total para esta calificación específica.
    total_score = models.FloatField(verbose_name="Puntuación Total")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de calificación")

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        # Un usuario solo puede calificar a un proveedor una vez.
        unique_together = ('provider', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Calificación de {self.user.username} para {self.provider.name}: {self.total_score}"

class Comment(models.Model):
    """
    Modelo para los comentarios que los usuarios dejan sobre los proveedores.
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='comments', verbose_name="Proveedor")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Usuario")
    body = models.TextField(verbose_name="Comentario")
    is_visible = models.BooleanField(default=True, verbose_name="Visible") # Para moderación del admin
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del comentario")

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-created_at']

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.provider.name}"