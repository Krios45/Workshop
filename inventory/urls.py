from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('history/', views.TransactionHistoryView.as_view(), name='transaction_history'),
    path('transaction/new/', views.CreateTransactionView.as_view(), name='create_transaction'),
]