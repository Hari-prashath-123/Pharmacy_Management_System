from django.core.management.base import BaseCommand
from inventory.models import Medicine
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with new sample medicines for testing various scenarios.'

    def handle(self, *args, **options):
        samples = [
            {'name': 'Azithromycin', 'category': 'Antibiotic', 'price': 45.00, 'stock_quantity': 15, 'manufacture_date': date(2024, 10, 15), 'expiry_date': date(2026, 10, 15)},
            {'name': 'Pantoprazole', 'category': 'Antacid', 'price': 12.50, 'stock_quantity': 8, 'manufacture_date': date(2025, 1, 10), 'expiry_date': date(2027, 1, 10)},
            {'name': 'Diclofenac', 'category': 'Painkiller', 'price': 8.75, 'stock_quantity': 50, 'manufacture_date': date(2024, 2, 1), 'expiry_date': date(2026, 2, 1)},
            {'name': 'Multivitamin Complex', 'category': 'Vitamin', 'price': 25.00, 'stock_quantity': 300, 'manufacture_date': date(2025, 3, 1), 'expiry_date': date(2028, 3, 1)},
            {'name': 'Cetirizine', 'category': 'Antihistamine', 'price': 3.25, 'stock_quantity': 100, 'manufacture_date': date(2024, 11, 20), 'expiry_date': date(2026, 11, 20)},
            {'name': 'Atorvastatin', 'category': 'Cholesterol', 'price': 24.50, 'stock_quantity': 45, 'manufacture_date': date(2025, 2, 10), 'expiry_date': date(2027, 2, 10)},
            {'name': 'Losartan', 'category': 'Blood Pressure', 'price': 14.20, 'stock_quantity': 60, 'manufacture_date': date(2024, 12, 5), 'expiry_date': date(2026, 12, 5)},
            {'name': 'Gabapentin', 'category': 'Nerve Pain', 'price': 32.75, 'stock_quantity': 30, 'manufacture_date': date(2025, 1, 20), 'expiry_date': date(2027, 1, 20)},
            {'name': 'Levothyroxine', 'category': 'Thyroid', 'price': 11.00, 'stock_quantity': 100, 'manufacture_date': date(2024, 10, 15), 'expiry_date': date(2026, 10, 15)},
            {'name': 'Sertraline', 'category': 'Antidepressant', 'price': 28.90, 'stock_quantity': 25, 'manufacture_date': date(2025, 3, 1), 'expiry_date': date(2027, 3, 1)},
            {'name': 'Amlodipine', 'category': 'Blood Pressure', 'price': 9.50, 'stock_quantity': 12, 'manufacture_date': date(2024, 11, 20), 'expiry_date': date(2026, 11, 20)},
            {'name': 'Montelukast', 'category': 'Asthma', 'price': 19.99, 'stock_quantity': 4, 'manufacture_date': date(2024, 9, 10), 'expiry_date': date(2026, 9, 10)},
            {'name': 'Prednisone', 'category': 'Steroid', 'price': 6.80, 'stock_quantity': 85, 'manufacture_date': date(2025, 4, 5), 'expiry_date': date(2027, 4, 5)},
            {'name': 'Pantoprazole', 'category': 'Antacid', 'price': 13.40, 'stock_quantity': 70, 'manufacture_date': date(2025, 1, 1), 'expiry_date': date(2027, 1, 1)},
            {'name': 'Meloxicam', 'category': 'NSAID', 'price': 15.25, 'stock_quantity': 55, 'manufacture_date': date(2024, 12, 12), 'expiry_date': date(2026, 12, 12)},
            {'name': 'Clopidogrel', 'category': 'Blood Thinner', 'price': 38.00, 'stock_quantity': 20, 'manufacture_date': date(2024, 8, 22), 'expiry_date': date(2026, 8, 22)},
            {'name': 'Albuterol Inhaler', 'category': 'Asthma', 'price': 45.50, 'stock_quantity': 15, 'manufacture_date': date(2025, 2, 28), 'expiry_date': date(2027, 2, 28)},
            {'name': 'Doxycycline', 'category': 'Antibiotic', 'price': 17.10, 'stock_quantity': 9, 'manufacture_date': date(2024, 11, 30), 'expiry_date': date(2026, 1, 15)},
            {'name': 'Hydrochlorothiazide', 'category': 'Diuretic', 'price': 5.25, 'stock_quantity': 110, 'manufacture_date': date(2025, 1, 10), 'expiry_date': date(2027, 1, 10)},
            {'name': 'Furosemide', 'category': 'Diuretic', 'price': 4.90, 'stock_quantity': 0, 'manufacture_date': date(2024, 10, 1), 'expiry_date': date(2026, 10, 1)},
            {'name': 'Warfarin', 'category': 'Blood Thinner', 'price': 22.00, 'stock_quantity': 35, 'manufacture_date': date(2025, 3, 15), 'expiry_date': date(2027, 3, 15)},
            {'name': 'Azithromycin', 'category': 'Antibiotic', 'price': 29.50, 'stock_quantity': 40, 'manufacture_date': date(2024, 7, 14), 'expiry_date': date(2026, 7, 14)},
            {'name': 'Metoprolol', 'category': 'Blood Pressure', 'price': 12.80, 'stock_quantity': 50, 'manufacture_date': date(2025, 2, 5), 'expiry_date': date(2027, 2, 5)},
            {'name': 'Tramadol', 'category': 'Painkiller', 'price': 35.00, 'stock_quantity': 18, 'manufacture_date': date(2024, 9, 30), 'expiry_date': date(2026, 9, 30)},
            {'name': 'Lorazepam', 'category': 'Anti-Anxiety', 'price': 21.40, 'stock_quantity': 2, 'manufacture_date': date(2024, 12, 20), 'expiry_date': date(2026, 12, 20)},
        ]
        created = 0
        for sample in samples:
            obj, was_created = Medicine.objects.get_or_create(
                name=sample['name'],
                defaults=sample
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} new sample medicines added to the database."))
