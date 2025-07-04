import time
import tracemalloc
import gc

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from docs.schemas import upload_response_schema, status_response_schema, api_info_response_schema, \
    metrics_response_schema
from .utils import data_format, calculate_metrics
from core.tfidf_app.serializers import FileUploadSerializer, MetricsInSerializer
from core.tfidf_app.models import Metrics
from core.tfidf_app.version import __version__
from ..doc_collections.services import DocumentModelAdapter


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )

    @upload_response_schema(request=FileUploadSerializer())
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data['file']

        file_name = file.name

        user = request.user.id

        DocumentModelAdapter.create_document(
            file=file,
            title=file_name,
            owner_id=user
        )

        gc.collect()

        tracemalloc.start()

        try:
            if hasattr(tracemalloc, 'reset_peak'):
                tracemalloc.reset_peak()

            start_time = time.perf_counter()

            result = data_format(file)

            end_time = time.perf_counter()

            _, peak = tracemalloc.get_traced_memory()

            elapsed_time = round(end_time - start_time, 3)

            data = {
                'file_name': file_name,
                'processing_time': elapsed_time,
                'status': 'success',
                'memory_usage': round(peak / 1024, 3)
            }

            metrics_data = MetricsInSerializer(data=data)
            metrics_data.is_valid()
            metrics_data = metrics_data.validated_data

            metric = Metrics.objects.create(
                file_name=metrics_data['file_name'],
                processing_time=metrics_data['processing_time'],
                status=metrics_data['status'],
                memory_usage=metrics_data['memory_usage']
            )

            metric.save()

            return Response({"result": result, 'processing_time': elapsed_time}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            tracemalloc.stop()


class MetricsView(APIView):

    @metrics_response_schema
    def get(self, request):
        metrics = calculate_metrics()

        data = {
            'files_processed': metrics['total_files'],
            'min_time_processed': metrics['min_time'],
            'avg_time_processed': metrics['avg_time'],
            'max_time_processed': metrics['max_time'],
            'latest_file_processed_timestamp': metrics['latest_file_processed'],
            'success_files': metrics['success_files'],
            'peak_memory_usage': metrics['peak_memory_usage'],
        }

        return Response(data=data, status=status.HTTP_200_OK)


class StatusGetView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @status_response_schema
    def get(self, request):
        print(request.user)
        return Response({"status": "Ok"}, status=status.HTTP_200_OK)


class ApiInfo(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @api_info_response_schema
    def get(self, request):
        data = {
            "name": "TF-IDF API",
            "version": __version__,
        }
        return Response(data, status=status.HTTP_200_OK)


def upload_file(request):
    """Загрузка и обработка файла, пагинация реализованна при помощи сессии, при закрытии браузера,
    сессия считается устаревшей"""
    page_obj = {}
    request_data = request.session.get('tfidf_data', [])

    if request.method == 'GET' and request_data:
        page_limit = 10
        data = request_data
        page_number = request.GET.get('page')
        page = Paginator(data, page_limit)
        page_obj = page.get_page(page_number)

    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            try:
                result = data_format(file)
                request.session['tfidf_data'] = result
                request.session.modified = True
                return redirect('upload')
            except Exception as e:
                error = f"Ошибка: {str(e)}"
        else:
            error = "Файл не загружен"
        return render(request, 'upload.html', {'error': error})
    return render(request, 'upload.html', {'data': page_obj})
