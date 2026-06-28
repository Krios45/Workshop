from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile

User = get_user_model()


class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
		'placeholder': 'example@company.com',
		'autocomplete': 'email',
	}))
	first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
		'placeholder': 'Họ của bạn',
		'autocomplete': 'given-name',
	}))
	last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
		'placeholder': 'Tên của bạn',
		'autocomplete': 'family-name',
	}))

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
			'placeholder': 'Tên đăng nhập',
			'autocomplete': 'username',
		})
		self.fields['password1'].widget.attrs.update({
			'placeholder': '••••••••',
			'autocomplete': 'new-password',
		})
		self.fields['password2'].widget.attrs.update({
			'placeholder': '••••••••',
			'autocomplete': 'new-password',
		})


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('phone', 'department', 'title')
