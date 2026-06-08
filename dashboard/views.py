from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def assets(request):
    return render(request, 'assets/list.html')


@login_required
def asset_detail(request):
    return render(request, 'assets/detail.html')


@login_required
def maintenance_schedule(request):
    context = {'success': request.method == 'POST'}
    return render(request, 'maintenance/schedule.html', context)


@login_required
def inventory(request):
    return render(request, 'inventory/list.html')


@login_required
def stock_transactions(request):
    context = {'success': request.method == 'POST'}
    return render(request, 'inventory/transactions.html', context)


@login_required
def analytics(request):
    return render(request, 'analytics.html')
