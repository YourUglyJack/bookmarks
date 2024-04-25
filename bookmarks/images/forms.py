from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in {'jpg', 'jpeg'}:
            raise forms.ValidationError('Error extension')
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image from the given URL
        res = request.urlopen(image_url)
        # image.image.save() 中的 save() 方法是 Django FieldFile 类的一个方法
        image.image.save(image_name, ContentFile(res.read()), save=False)
        if commit:
            image.save()
        return image