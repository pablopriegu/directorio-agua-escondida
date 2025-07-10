from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from directorio_api.models import Category
import os

class Command(BaseCommand):
    help = 'Creates a superuser and initial categories if they do not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # --- Crear Superusuario ---
        ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
        ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

        if ADMIN_USERNAME and not User.objects.filter(username=ADMIN_USERNAME).exists():
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser creation skipped (already exists or env vars not set).'))

        # --- Crear Categorías ---
        initial_categories = ['Albañilería', 'Plomería', 'Electricidad', 'Carpintería', 'Jardinería']
        for cat_name in initial_categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{cat_name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{cat_name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Initial data setup complete.'))