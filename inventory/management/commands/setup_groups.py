from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from inventory.models import Medicine


class Command(BaseCommand):
    help = 'Set up user groups and permissions for Pharmacy Management System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Setting up groups and permissions...'))
        
        # Get Medicine content type
        medicine_ct = ContentType.objects.get_for_model(Medicine)
        
        # Get or create permissions
        view_permission = Permission.objects.get(codename='view_medicine', content_type=medicine_ct)
        add_permission = Permission.objects.get(codename='add_medicine', content_type=medicine_ct)
        change_permission = Permission.objects.get(codename='change_medicine', content_type=medicine_ct)
        delete_permission = Permission.objects.get(codename='delete_medicine', content_type=medicine_ct)
        
        # Create Manager Group
        manager_group, created = Group.objects.get_or_create(name='Manager')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Manager group'))
        else:
            self.stdout.write(self.style.WARNING('○ Manager group already exists'))
        
        # Assign all permissions to Manager group
        manager_group.permissions.set([
            view_permission,
            add_permission,
            change_permission,
            delete_permission
        ])
        self.stdout.write(self.style.SUCCESS('✓ Assigned all permissions to Manager group'))
        self.stdout.write(self.style.SUCCESS('  - View medicines'))
        self.stdout.write(self.style.SUCCESS('  - Add medicines'))
        self.stdout.write(self.style.SUCCESS('  - Update medicines'))
        self.stdout.write(self.style.SUCCESS('  - Delete medicines'))
        
        # Create Staff Group
        staff_group, created = Group.objects.get_or_create(name='Staff')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Staff group'))
        else:
            self.stdout.write(self.style.WARNING('○ Staff group already exists'))
        
        # Assign view and change permissions to Staff group (no delete)
        staff_group.permissions.set([
            view_permission,
            add_permission,
            change_permission
        ])
        self.stdout.write(self.style.SUCCESS('✓ Assigned limited permissions to Staff group'))
        self.stdout.write(self.style.SUCCESS('  - View medicines'))
        self.stdout.write(self.style.SUCCESS('  - Add medicines'))
        self.stdout.write(self.style.SUCCESS('  - Update medicines'))
        self.stdout.write(self.style.WARNING('  - NO delete permission'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Groups and Permissions Setup Complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nGroup Summary:')
        self.stdout.write(f'  • Manager: Full access (view, add, update, delete)')
        self.stdout.write(f'  • Staff: Limited access (view, add, update only)')
        self.stdout.write('\nNext Steps:')
        self.stdout.write('  1. Assign users to groups via Django Admin')
        self.stdout.write('  2. Test permissions with different user accounts')
