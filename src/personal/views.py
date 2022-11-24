from django.shortcuts import render, redirect
from personal.forms import UploadPhotoForm
from account.models import Account 
from personal.models import Bio
import string
import random

# Create your views here.

context = {}

def home_screen_view(request):

	user = request.user

	photos = Bio.objects.filter(author=user).order_by('-id')[:1]

	context = {
		"photos": photos
	}
	return render(request, 'personal/home.html', context)

def profile_photo_view(request):

	user = request.user
	if not user.is_authenticated:
		return redirect('login')
	
	photos = Bio.objects.filter(author=user).order_by('-id')[:1]

	

	form = UploadPhotoForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.title = random.choice(string.ascii_letters)
		obj.save()
		return redirect('home')

	context = {
		"form": form,
		"photos": photos
	}
	return render(request, 'personal/profile_photo.html', context)
