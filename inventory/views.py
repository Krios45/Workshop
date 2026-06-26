from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import F
from .models import Material, StockTransaction
from .forms import StockTransactionForm

class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    template_name = 'inventory/material_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)

        low_stock = self.request.GET.get('low_stock')
        if low_stock == 'true':
            queryset = queryset.filter(quantity__lte=F('min_quantity'))
            
        return queryset

class TransactionHistoryView(LoginRequiredMixin, ListView):
    model = StockTransaction
    template_name = 'inventory/transaction_history.html'
    context_object_name = 'logs'

class CreateTransactionView(LoginRequiredMixin, CreateView):
    model = StockTransaction
    form_class = StockTransactionForm
    template_name = 'inventory/log_form.html'
    success_url = reverse_lazy('inventory:transaction_history')

    def form_valid(self, form):
        form.instance.user = self.request.user
        transaction = form.save(commit=False)
        material = transaction.material

        if transaction.transaction_type == 'import':
            material.quantity += transaction.quantity 
        elif transaction.transaction_type == 'export':
            material.quantity -= transaction.quantity 
            
        material.save()
        return super().form_valid(form)