from django import forms
from personal.models import Bio 



class UploadPhotoForm(forms.ModelForm):

	class Meta:
		model = Bio
		fields = ['image']