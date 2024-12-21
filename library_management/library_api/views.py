from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .models import Author, Book, BorrowRecord
from .serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer
from library_management.tasks import generate_report
import os
import json


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    @action(detail=True, methods=['put'], url_path='return')
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()
        if not borrow_record.return_date:
            borrow_record.return_date = datetime.now().date()
            borrow_record.book.available_copies += 1
            borrow_record.book.save()
            borrow_record.save()
            return Response({'status': 'Book returned successfully'})
        else:
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        book = Book.objects.get(id=request.data['book'])
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            return super().create(request, *args, **kwargs)
        else:
            return Response({'error': 'No available copies'}, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='')
    def get_latest_report(self, request):
        report_dir = 'library_management/reports'
        if not os.path.exists(report_dir):
            return Response({'error': 'No reports available'}, status=status.HTTP_404_NOT_FOUND)

        files = sorted(os.listdir(report_dir), reverse=True)
        if not files:
            return Response({'error': 'No reports available'}, status=status.HTTP_404_NOT_FOUND)

        latest_report_file = os.path.join(report_dir, files[0])
        with open(latest_report_file, 'r') as f:
            report = json.load(f)
        return Response(report)

    @action(detail=False, methods=['post'], url_path='')
    def create_report(self, request):
        generate_report()
        return Response({'status': 'Report generation started'})
