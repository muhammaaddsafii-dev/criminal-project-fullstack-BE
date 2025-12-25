# core/management/commands/create_default_users.py
# Buat folder: core/management/commands/ jika belum ada

from django.core.management.base import BaseCommand
from core.models import User


class Command(BaseCommand):
    help = 'Create default users for testing'

    def handle(self, *args, **kwargs):
        # Create superuser/admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@kriminalitas.com',
                password='admin123',
                name='Administrator',
                jabatan='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created'))
        
        # Create operator
        if not User.objects.filter(username='operator').exists():
            User.objects.create_user(
                username='operator',
                email='operator@kriminalitas.com',
                password='operator123',
                name='Operator Sistem',
                jabatan='operator'
            )
            self.stdout.write(self.style.SUCCESS('User "operator" created'))
        
        # Create viewer
        if not User.objects.filter(username='viewer').exists():
            User.objects.create_user(
                username='viewer',
                email='viewer@kriminalitas.com',
                password='viewer123',
                name='Viewer',
                jabatan='viewer'
            )
            self.stdout.write(self.style.SUCCESS('User "viewer" created'))
        
        self.stdout.write(self.style.SUCCESS('All default users have been created'))