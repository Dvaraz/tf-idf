from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .utils import data_format


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
