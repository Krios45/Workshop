from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Asset, MaintenanceLog, AssetCategory
from .forms import AssetForm

def is_manager_or_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__in=['Admin', 'Manager']).exists())

@login_required
def asset_list(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    assets = Asset.objects.all().order_by('-created_at')
    
    if query:
        assets = assets.filter(Q(name__icontains=query) | Q(code__icontains=query) | Q(serial_number__icontains=query))
    
    if status_filter:
        assets = assets.filter(status=status_filter)
        
    context = {
        'assets': assets,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Asset.STATUS_CHOICES,
        'is_manager': is_manager_or_admin(request.user),
    }
    return render(request, 'assets/list.html', context)

@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    maintenance_logs = asset.maintenance_logs.all().order_by('-start_date')
    # Fetch recent bookings for this asset
    bookings = asset.bookings.all().order_by('-start_time')[:10]
    
    context = {
        'asset': asset,
        'maintenance_logs': maintenance_logs,
        'bookings': bookings,
        'is_manager': is_manager_or_admin(request.user),
    }
    return render(request, 'assets/detail.html', context)

@login_required
@user_passes_test(is_manager_or_admin, login_url='accounts:login')
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f"Đã thêm thiết bị {asset.name} thành công.")
            return redirect('assets:list')
    else:
        form = AssetForm()
        
    return render(request, 'assets/form.html', {'form': form, 'title': 'Thêm thiết bị mới'})

@login_required
@user_passes_test(is_manager_or_admin, login_url='accounts:login')
def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f"Đã cập nhật thiết bị {asset.name} thành công.")
            return redirect('assets:detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)
        
    return render(request, 'assets/form.html', {'form': form, 'title': 'Chỉnh sửa thiết bị', 'asset': asset})

@login_required
@user_passes_test(is_manager_or_admin, login_url='accounts:login')
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        name = asset.name
        asset.delete()
        messages.success(request, f"Đã xóa thiết bị {name} thành công.")
        return redirect('assets:list')
    return render(request, 'assets/confirm_delete.html', {'asset': asset})
