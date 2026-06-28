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


from django.http import JsonResponse
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

@login_required
def diagnose(request):
    # Only allow superusers to access diagnostics
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    db_engine = connection.vendor
    
    # Check assets
    try:
        from assets.models import Asset, AssetCategory
        asset_count = Asset.objects.count()
        category_count = AssetCategory.objects.count()
        assets_list = list(Asset.objects.values('code', 'name', 'status')[:10])
    except Exception as e:
        asset_count = f"Error: {str(e)}"
        category_count = f"Error: {str(e)}"
        assets_list = []

    # Check materials
    try:
        from inventory.models import Material
        material_count = Material.objects.count()
        materials_list = list(Material.objects.values('name')[:10])
    except Exception as e:
        material_count = f"Error: {str(e)}"
        materials_list = []

    # Check migrations
    try:
        applied_migrations = list(MigrationRecorder.Migration.objects.values('app', 'name', 'applied'))
    except Exception as e:
        applied_migrations = f"Error: {str(e)}"

    return JsonResponse({
        'database_engine': db_engine,
        'asset_count': asset_count,
        'category_count': category_count,
        'assets_sample': assets_list,
        'material_count': material_count,
        'materials_sample': materials_list,
        'applied_migrations': applied_migrations,
    })

