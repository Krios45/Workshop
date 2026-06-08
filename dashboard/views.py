from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from assets.models import Asset
from bookings.models import Booking
from inventory.models import Material

def home(request):
    total_assets = Asset.objects.count()
    active_assets = Asset.objects.filter(status=Asset.STATUS_AVAILABLE).count()
    maintenance_assets = Asset.objects.filter(status=Asset.STATUS_MAINTENANCE).count()
    total_materials = Material.objects.count()
    
    context = {
        'total_assets': total_assets,
        'active_assets': active_assets,
        'maintenance_assets': maintenance_assets,
        'total_materials': total_materials,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    total_assets = Asset.objects.count()
    active_assets = Asset.objects.filter(status=Asset.STATUS_AVAILABLE).count()
    in_use_assets = Asset.objects.filter(status=Asset.STATUS_IN_USE).count()
    error_assets = Asset.objects.filter(status=Asset.STATUS_RETIRED).count() + Asset.objects.filter(status=Asset.STATUS_MAINTENANCE).count()
    bookings_count = Booking.objects.count()
    
    # Recent Bookings for activity feed
    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_assets': total_assets,
        'active_assets': active_assets,
        'in_use_assets': in_use_assets,
        'error_assets': error_assets,
        'bookings_count': bookings_count,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard.html', context)


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

