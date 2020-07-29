from django import forms
from django.forms import ModelForm
from .models import Lecture

class LectureForm(forms.ModelForm):

	class Meta:

		model = Lecture
		fields = '__all__'