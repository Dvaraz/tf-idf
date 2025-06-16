import math
import re

from collections import defaultdict
from django.db.models import Min, Max, Avg, Count, Q

from core.tfidf_app.models import Metrics


def preprocess_text(file) -> list[str]:
    """Чтение и разделение на документы (по строкам)"""
    documents = []
    for line in file:
        line = line.decode('utf-8').strip()
        if line:
            documents.append(line)

    # Удаление пунктуации и приведение к нижнему регистру.
    processed_docs = []
    for doc in documents:
        doc = doc.lower()
        doc = re.sub(r'[^\w\s]', ' ', doc)
        processed_docs.append(doc.split())

    return processed_docs


def clean_text(text: str) -> str:
    text = text.lower()
    doc = re.sub(r'[^\w\s]', ' ', text)
    return doc


def compute_tf(text: str) -> dict:
    """Вычисление TF для документа."""
    tf = defaultdict(float)
    words = text
    total_words = len(words)
    for word in words:
        tf[word] += 1
    # Нормализация
    for word in tf:
        tf[word] /= total_words
    return tf


def compute_tf_for_corpus(file) -> dict:

    tfs = defaultdict(str)
    for doc_number, document in enumerate(file, 1):
        tfs[f'Doc {doc_number}'] = compute_tf(document)

    return tfs


def compute_idf(documents) -> tuple:
    """Вычисление IDF для корпуса."""
    idf = defaultdict(float)
    total_documents = len(documents)

    # Счетчик сколько раз это слово встречается в корпусе
    tf_total = defaultdict(int)

    # Счетчик документов, содержащих каждое слово
    doc_count = defaultdict(int)

    for words in documents:
        unique_words = set(words)
        for word in unique_words:
            doc_count[word] += 1
        for word in words:
            tf_total[word] += 1

    idf = {word: math.log10(total_documents / doc_count[word]) if doc_count[word] else 0 for word in tf_total}

    return idf, tf_total


def data_format(file):
    processed_docs = preprocess_text(file)

    tf_list = compute_tf_for_corpus(processed_docs)

    idf, tf_total = compute_idf(processed_docs)

    # Формирование данных
    data = [{
        'word': word,
        'tf': tf_total[word],
        'docs': {key: item[word] for key, item in tf_list.items()},
        'idf': round(idf[word], 4)
    } for word in tf_total]

    # Сортировка и выбор топ-50
    return sorted(data, key=lambda x: -x['idf'])[:50]


def compute_tf_idf_for_document(doc_text: str, collection: list[list[str]]):
    tf = compute_tf(doc_text)
    idf, _ = compute_idf(collection)

    data = [
        {
            'word': word,
            'tf': tf[word],
            'idf': idf[word]
        }
        for word in tf
    ]

    return sorted(data, key=lambda x: x['tf'])[:50]


def calculate_metrics():

    metrics = Metrics.objects.aggregate(
        total_files=Count('id'),
        min_time=Min('processing_time'),
        avg_time=Avg('processing_time'),
        max_time=Max('processing_time'),
        latest_file_processed=Max('processed_timestamp'),
        success_files=Count('id', filter=Q(status='success')),
        peak_memory_usage=Max('memory_usage'),
    )

    latest_file_processed = metrics.get('latest_file_processed')
    metrics['latest_file_processed'] = latest_file_processed.strftime('%Y-%m-%d %H:%M:%S') if \
        latest_file_processed else 'N/A'

    return metrics
