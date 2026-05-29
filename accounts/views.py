from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm, UserProfileForm, UserUpdateForm
from .models import UserProfile


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('dashboard:dashboard')
	else:
		form = SignUpForm()

	return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
	profile, _ = UserProfile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = UserProfileForm(request.POST, instance=profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('accounts:profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = UserProfileForm(instance=profile)

	context = {
		'user_form': user_form,
		'profile_form': profile_form,
	}
	return render(request, 'accounts/profile.html', context)
