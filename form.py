from django import forms
from django.forms import ModelForm
from django.forms import CharField
from django.forms import IntegerField
from django.forms import DecimalField
from models import UserImage

class UserImageForm(ModelForm):
	class Meta:
		model = UserImage

	latitude = forms.DecimalField(required=False)
	longitude = forms.DecimalField(required=False)
	image_url = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super(UserImageForm, self).clean()
		return cleaned_data
