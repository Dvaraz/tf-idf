from django.urls import path
from core.doc_collections import views

urlpatterns = [
    path('documents/', views.DocumentsListView.as_view(), name='documents_list'),
    path(
        'documents/<int:pk>/',
        views.DocumentContentView.as_view({'get': 'get_content', 'delete': 'destroy'}),
        name='document_content'
    ),
    path(
        'documents/<int:pk>/statistics/',
        views.DocumentStatisticView.as_view({'get': 'statistics'}),
        name='document_statistics'
    ),
    path(
        'documents/<int:pk>/huffman/',
        views.DocumentHuffmanView.as_view({'get': 'huffman_encode'}),
        name='document_huffman'
    ),
    path('collections/', views.CollectionListView.as_view(), name='collections_list'),
    path('collections/create/', views.CollectionCreateView.as_view(), name='collections_create'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path(
        'collections/<int:pk>/statistics/',
        views.CollectionStatisticView.as_view({'get': 'statistics'}),
        name='collection_statistics'
    ),
    path(
        'collections/<int:pk>/<int:document_id>/',
        views.CollectionModifyView.as_view({'post': 'modify_collection', 'delete': 'modify_collection'}),
        name='collections_modify')
]
