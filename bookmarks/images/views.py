from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image


# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    return render(request, 'images/image/create.html', {'form': form, 'section': 'images'})


def image_detail(request, *args, **kwargs):
    image = get_object_or_404(Image, id=kwargs['id'], slug=kwargs['slug'])
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})