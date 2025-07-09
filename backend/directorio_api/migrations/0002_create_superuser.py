from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    User = apps.get_model('directorio_api', 'User')

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com') # Email opcional

    if ADMIN_USERNAME and ADMIN_PASSWORD and not User.objects.filter(username=ADMIN_USERNAME).exists():
        User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
        print('Superuser created successfully.')
    else:
        print('Superuser not created. Check environment variables or if user already exists.')

class Migration(migrations.Migration):

    dependencies = [
        ('directorio_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]