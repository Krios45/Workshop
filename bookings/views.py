from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from assets.models import Asset
from .models import Booking
from .forms import BookingForm

def is_manager_or_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__in=['Admin', 'Manager']).exists())

@login_required
def booking_list(request):
    is_manager = is_manager_or_admin(request.user)
    if is_manager:
        bookings = Booking.objects.all().order_by('-created_at')
    else:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        
    context = {
        'bookings': bookings,
        'is_manager': is_manager,
    }
    return render(request, 'bookings/list.html', context)

@login_required
def booking_create(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    
    # Check if asset is available for booking
    if asset.status != Asset.STATUS_AVAILABLE:
        messages.error(request, f"Thiết bị {asset.name} đang ở trạng thái '{asset.get_status_display()}'. Chỉ có thể đặt lịch khi thiết bị sẵn sàng.")
        return redirect('assets:detail', pk=asset.pk)
        
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.asset = asset
            booking.status = Booking.STATUS_PENDING
            
            start_time = booking.start_time
            end_time = booking.end_time
            
            # Check overlap with APPROVED bookings for this asset
            overlap = Booking.objects.filter(
                asset=asset,
                status=Booking.STATUS_APPROVED,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if overlap.exists():
                form.add_error(None, "Thiết bị này đã có lịch đặt khác được phê duyệt trong khoảng thời gian đã chọn.")
            else:
                booking.save()
                messages.success(request, f"Đã đăng ký đặt lịch thiết bị {asset.name} thành công. Vui lòng chờ phê duyệt.")
                return redirect('bookings:list')
    else:
        form = BookingForm(initial={'asset': asset})
        
    context = {
        'form': form,
        'asset': asset,
    }
    return render(request, 'bookings/create.html', context)

@login_required
@user_passes_test(is_manager_or_admin, login_url='accounts:login')
def booking_approve(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.status == Booking.STATUS_PENDING:
        asset = booking.asset
        # Update asset status to IN_USE
        asset.status = Asset.STATUS_IN_USE
        asset.save()
        
        booking.status = Booking.STATUS_APPROVED
        booking.save()
        messages.success(request, f"Đã phê duyệt lịch đặt của {booking.user.username} cho {asset.name}.")
    else:
        messages.error(request, "Lịch đặt này không ở trạng thái chờ duyệt.")
    return redirect('bookings:list')

@login_required
@user_passes_test(is_manager_or_admin, login_url='accounts:login')
def booking_reject(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.status == Booking.STATUS_PENDING:
        booking.status = Booking.STATUS_REJECTED
        booking.save()
        messages.success(request, f"Đã từ chối lịch đặt của {booking.user.username} cho {booking.asset.name}.")
    else:
        messages.error(request, "Lịch đặt này không ở trạng thái chờ duyệt.")
    return redirect('bookings:list')

@login_required
@user_passes_test(is_manager_or_admin, login_url='accounts:login')
def booking_return(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.status == Booking.STATUS_APPROVED:
        asset = booking.asset
        asset.status = Asset.STATUS_AVAILABLE
        asset.save()
        
        booking.status = Booking.STATUS_COMPLETED
        booking.save()
        messages.success(request, f"Đã xác nhận trả thiết bị {asset.name} thành công.")
    else:
        messages.error(request, "Chỉ có thể trả thiết bị cho lịch đặt đã duyệt.")
    return redirect('bookings:list')

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Users can only cancel their own bookings, managers can cancel any
    if booking.user == request.user or is_manager_or_admin(request.user):
        if booking.status in [Booking.STATUS_PENDING, Booking.STATUS_APPROVED]:
            asset = booking.asset
            if booking.status == Booking.STATUS_APPROVED:
                # Set asset back to available if it was approved and in use
                asset.status = Asset.STATUS_AVAILABLE
                asset.save()
                
            booking.status = Booking.STATUS_CANCELED
            booking.save()
            messages.success(request, "Đã hủy lịch đặt thành công.")
        else:
            messages.error(request, "Không thể hủy lịch đặt ở trạng thái hiện tại.")
    else:
        messages.error(request, "Bạn không có quyền hủy lịch đặt này.")
    return redirect('bookings:list')


@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Only owner or manager can edit, and only when pending
    if booking.user != request.user and not is_manager_or_admin(request.user):
        messages.error(request, "Bạn không có quyền chỉnh sửa lịch đặt này.")
        return redirect('bookings:list')

    if booking.status != Booking.STATUS_PENDING:
        messages.error(request, "Chỉ có thể chỉnh sửa lịch đặt đang chờ duyệt.")
        return redirect('bookings:list')

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated = form.save(commit=False)
            start_time = updated.start_time
            end_time = updated.end_time

            # Check overlap with APPROVED bookings for this asset (exclude self)
            overlap = Booking.objects.filter(
                asset=booking.asset,
                status=Booking.STATUS_APPROVED,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(pk=booking.pk)

            if overlap.exists():
                form.add_error(None, "Thiết bị này đã có lịch được phê duyệt trong khoảng thời gian đã chọn.")
            else:
                updated.save()
                messages.success(request, "Đã cập nhật lịch đặt thành công.")
                return redirect('bookings:list')
    else:
        form = BookingForm(instance=booking)

    context = {
        'form': form,
        'booking': booking,
        'asset': booking.asset,
        'is_edit': True,
    }
    return render(request, 'bookings/edit.html', context)


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Only owner or manager can delete, and only when pending
    if booking.user != request.user and not is_manager_or_admin(request.user):
        messages.error(request, "Bạn không có quyền xóa lịch đặt này.")
        return redirect('bookings:list')

    if booking.status != Booking.STATUS_PENDING:
        messages.error(request, "Chỉ có thể xóa lịch đặt đang chờ duyệt.")
        return redirect('bookings:list')

    if request.method == 'POST':
        asset_name = booking.asset.name
        booking.delete()
        messages.success(request, f"Đã xóa lịch đặt thiết bị {asset_name} thành công.")
        return redirect('bookings:list')

    return render(request, 'bookings/delete_confirm.html', {'booking': booking})
