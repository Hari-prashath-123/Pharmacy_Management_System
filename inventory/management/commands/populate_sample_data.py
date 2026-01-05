from django.core.management.base import BaseCommand
from inventory.models import Medicine
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with 10 sample medicine records for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating database with sample medicine records...'))
        
        # Clear existing data (optional - comment out if you want to keep existing records)
        # Medicine.objects.all().delete()
        # self.stdout.write(self.style.WARNING('Cleared existing medicine records'))
        
        # Sample medicine data
        medicines_data = [
            {
                'name': 'Aspirin',
                'category': 'Painkiller',
                'price': 5.99,
                'stock_quantity': 150,
                'manufacture_date': date(2025, 1, 15),
                'expiry_date': date(2027, 1, 15)
            },
            {
                'name': 'Amoxicillin',
                'category': 'Antibiotic',
                'price': 12.50,
                'stock_quantity': 80,
                'manufacture_date': date(2024, 11, 1),
                'expiry_date': date(2026, 11, 1)
            },
            {
                'name': 'Ibuprofen',
                'category': 'Painkiller',
                'price': 7.25,
                'stock_quantity': 200,
                'manufacture_date': date(2025, 3, 10),
                'expiry_date': date(2027, 3, 10)
            },
            {
                'name': 'Paracetamol',
                'category': 'Fever Reducer',
                'price': 4.50,
                'stock_quantity': 5,  # Low stock
                'manufacture_date': date(2024, 6, 20),
                'expiry_date': date(2026, 6, 20)
            },
            {
                'name': 'Metformin',
                'category': 'Diabetes',
                'price': 15.75,
                'stock_quantity': 120,
                'manufacture_date': date(2025, 2, 5),
                'expiry_date': date(2027, 2, 5)
            },
            {
                'name': 'Lisinopril',
                'category': 'Blood Pressure',
                'price': 18.99,
                'stock_quantity': 95,
                'manufacture_date': date(2024, 12, 1),
                'expiry_date': date(2026, 12, 1)
            },
            {
                'name': 'Omeprazole',
                'category': 'Antacid',
                'price': 9.99,
                'stock_quantity': 3,  # Low stock
                'manufacture_date': date(2024, 8, 15),
                'expiry_date': date(2026, 1, 20)  # Expiring soon (within 30 days)
            },
            {
                'name': 'Ciprofloxacin',
                'category': 'Antibiotic',
                'price': 22.50,
                'stock_quantity': 60,
                'manufacture_date': date(2024, 5, 10),
                'expiry_date': date(2026, 5, 10)
            },
            {
                'name': 'Vitamin D3',
                'category': 'Vitamin',
                'price': 11.25,
                'stock_quantity': 180,
                'manufacture_date': date(2025, 4, 1),
                'expiry_date': date(2028, 4, 1)
            },
            {
                'name': 'Expired Medicine Sample',
                'category': 'Test Category',
                'price': 10.00,
                'stock_quantity': 0,  # Out of stock
                'manufacture_date': date(2023, 1, 1),
                'expiry_date': date(2025, 1, 1)  # Already expired
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for medicine_data in medicines_data:
            medicine, created = Medicine.objects.get_or_create(
                name=medicine_data['name'],
                defaults=medicine_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {medicine.name}'))
            else:
                # Update existing medicine
                for key, value in medicine_data.items():
                    setattr(medicine, key, value)
                medicine.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'○ Updated: {medicine.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('Sample Data Population Complete!'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(f'\nStatistics:')
        self.stdout.write(f'  • New records created: {created_count}')
        self.stdout.write(f'  • Existing records updated: {updated_count}')
        self.stdout.write(f'  • Total medicines in database: {Medicine.objects.count()}')
        
        self.stdout.write('\n' + 'Sample Data Details:')
        self.stdout.write('  • Regular stock: 7 medicines')
        self.stdout.write('  • Low stock (≤10): 3 medicines')
        self.stdout.write('  • Expiring soon (within 30 days): 1 medicine')
        self.stdout.write('  • Already expired: 1 medicine')
        self.stdout.write('  • Out of stock: 1 medicine')
        
        self.stdout.write('\n' + 'Next Steps:')
        self.stdout.write('  1. Run server: python manage.py runserver')
        self.stdout.write('  2. Login at: http://127.0.0.1:8000/login/')
        self.stdout.write('  3. View dashboard to see sample data')
