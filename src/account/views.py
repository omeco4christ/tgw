from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

from account.models import Account
from personal.models import Bio



# Create your views here.
context = {}
def login_view(request):

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect('home')

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'account/login.html', context)




def signup_view(request):
	user = request.user
	if user.is_authenticated:
		return redirect('home')

	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/signup.html', context)


def forgot_password_view(request):
	return render(request, 'account/forgot-password.html', context)



def logout_view(request):
	logout(request)
	return redirect('home')


def account_view(request):
	user = request.user
	if not request.user.is_authenticated:
		return redirect('login')

	photos = Bio.objects.filter(author=user).order_by('-id')[:1]

	if request.POST:
		form = AccountUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
				"first_name": request.POST['first_name'],
				"last_name": request.POST['last_name'],
			}
			form.save()
			return redirect('home')
	else:
		form = AccountUpdateForm(
				initial = {
					"email": request.user.email,
					"username": request.user.username,
					"first_name": request.user.first_name,
					"last_name": request.user.last_name,
				}
			)

	context['account_form'] = form
	context['photos'] = photos
	return render(request, 'account/account.html', context)



