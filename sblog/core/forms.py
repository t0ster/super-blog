from django import forms
from django.forms.models import modelformset_factory

from sblog.core.models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


ImageFormSet = modelformset_factory(Image, ImageForm, extra=1)