from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Create demo users for testing authentication'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating demo users...'))
        
        # Get groups
        try:
            manager_group = Group.objects.get(name='Manager')
            staff_group = Group.objects.get(name='Staff')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Groups not found! Run: python manage.py setup_groups'))
            return
        
        # Create Manager User
        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user(
                username='manager',
                email='manager@pharmacy.com',
                password='manager123',
                first_name='John',
                last_name='Manager'
            )
            manager.groups.add(manager_group)
            self.stdout.write(self.style.SUCCESS('✓ Created Manager user'))
            self.stdout.write(self.style.SUCCESS('  Username: manager'))
            self.stdout.write(self.style.SUCCESS('  Password: manager123'))
        else:
            self.stdout.write(self.style.WARNING('○ Manager user already exists'))
        
        # Create Staff User
        if not User.objects.filter(username='staff').exists():
            staff = User.objects.create_user(
                username='staff',
                email='staff@pharmacy.com',
                password='staff123',
                first_name='Jane',
                last_name='Staff'
            )
            staff.groups.add(staff_group)
            self.stdout.write(self.style.SUCCESS('✓ Created Staff user'))
            self.stdout.write(self.style.SUCCESS('  Username: staff'))
            self.stdout.write(self.style.SUCCESS('  Password: staff123'))
        else:
            self.stdout.write(self.style.WARNING('○ Staff user already exists'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Demo Users Created Successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('  Manager Account:')
        self.stdout.write('    Username: manager')
        self.stdout.write('    Password: manager123')
        self.stdout.write('    Permissions: View, Add, Update, Delete')
        self.stdout.write('')
        self.stdout.write('  Staff Account:')
        self.stdout.write('    Username: staff')
        self.stdout.write('    Password: staff123')
        self.stdout.write('    Permissions: View, Add, Update (No Delete)')
        self.stdout.write('')
        self.stdout.write('Login at: http://127.0.0.1:8000/login/')
