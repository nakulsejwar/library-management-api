from celery import shared_task
from library_api.models import Author, Book, BorrowRecord
import json
import os
from datetime import datetime

@shared_task
def generate_report():
    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    total_borrowed_books = BorrowRecord.objects.filter(return_date__isnull=True).count()

    report = {
        'total_authors': total_authors,
        'total_books': total_books,
        'total_borrowed_books': total_borrowed_books,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save report to a JSON file
    report_dir = 'library_management/reports'
    os.makedirs(report_dir, exist_ok=True)
    report_file = os.path.join(report_dir, f'report_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json')
    with open(report_file, 'w') as f:
        json.dump(report, f)

    return report_file
