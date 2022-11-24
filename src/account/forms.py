from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import authenticate

from account.models import Account 


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

	class Meta:
		model = Account
		fields = ("email", "username", "first_name", "last_name", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid Login")

class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username', 'first_name', 'last_name')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use' % email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use' % username)

	# def clean_first_name(self):
	# 	if self.is_valid():
	# 		first_name = self.cleaned_data['first_name']
	# 		try:
	# 			account = Account.objects.exclude(pk=self.instance.pk).get(first_name=first_name)
	# 		except Account.DoesNotExist:
	# 			return first_name
	# 		raise forms.ValidationError('First Name "%s" is already in use' % first_name)


	# def clean_last_name(self):
	# 	if self.is_valid():
	# 		last_name = self.cleaned_data['last_name']
	# 		try:
	# 			account = Account.objects.exclude(pk=self.instance.pk).get(last_name=last_name)
	# 		except Account.DoesNotExist:
	# 			return last_name
	# 		raise forms.ValidationError('Last Name "%s" is already in use' % last_name)