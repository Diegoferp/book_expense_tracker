import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from books.models import Book


class Command(BaseCommand):
    """
    Load books from a CSV file.
    - If there's a duplicate 'id' in the DB, generate a new one by appending '-1', '-2', etc.
    - Attempts to parse 'published_date' in MM/DD/YYYY format. If invalid, uses None.
    """
    help = 'Load books from CSV file, auto-fix duplicate IDs, and handle date parsing.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        self.stdout.write(self.style.SUCCESS(f'Loading books from {csv_file}...'))

        try:
            with open(csv_file, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)

                # Show the headers that are detected (for debugging)
                self.stdout.write(f"Detected CSV headers: {reader.fieldnames}")

                for row in reader:
                    original_id = row['id']

                    # -- Parse date --
                    date_str = row.get('published_date', '')  # or the CSV column name
                    published_date = None
                    try:
                        # Expect "MM/DD/YYYY" like "07/10/2019"
                        published_date = datetime.strptime(date_str, "%m/%d/%Y").date()
                    except ValueError:
                        # If invalid or empty, handle however you like (assign None, skip, etc.)
                        self.stdout.write(self.style.WARNING(
                            f"Invalid date '{date_str}' for row ID={original_id}. Storing None."
                        ))

                    # -- Generate unique ID if a row with this ID already exists --
                    new_id = original_id
                    suffix = 1
                    while Book.objects.filter(id=new_id).exists():
                        new_id = f"{original_id}-{suffix}"
                        suffix += 1

                    try:
                        # Create the Book record
                        Book.objects.create(
                            id=new_id,
                            title=row['title'],
                            subtitle=row['subtitle'],
                            authors=row['authors'],
                            publisher=row['publisher'],
                            published_date=published_date,
                            category=row['category'],
                            distribution_expense=row['distribution_expense'],
                        )
                    except IntegrityError as e:
                        # This catches any other DB constraint issues
                        self.stdout.write(self.style.ERROR(
                            f"Failed to insert row with original ID={original_id} (new ID={new_id}). Reason: {e}"
                        ))
                        # You can choose to continue or break
                        continue

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        self.stdout.write(self.style.SUCCESS("Successfully loaded books."))
