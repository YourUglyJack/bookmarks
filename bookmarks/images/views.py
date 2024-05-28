from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action


# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    return render(request, 'images/image/create.html', {'form': form, 'section': 'images'})


def image_detail(request, *args, **kwargs):
    image = get_object_or_404(Image, id=kwargs['id'], slug=kwargs['slug'])
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        # image.users_like 不是一个列表，而是一个 ManyToMany 关系的管理器。你不能直接对其调用 len() 函数，也不能直接在列表推导式中使用它。你需要调用它的 all()
        # 方法来获取一个包含所有相关对象的查询集，然后你可以在这个查询集上使用 len() 函数或者列表推导式
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            if image.users_like.count() > 0:
                users_likes = [{'url': user.profile.photo.url, 'first_name': user.first_name} for user in
                               image.users_like.all()]
            else:
                users_likes = []
            return JsonResponse({'status': 'ok', 'users_like': users_likes})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    # todo 开始时没有滚动条的话，就无法拉到窗口底部发起ajax请求获取更多的图片，但是更改窗口大小即可；不知道改怎么修复
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # 在许多使用 AJAX 的无限滚动或分页系统中，当用户滚动到页面底部时，会自动发送一个 AJAX 请求以获取更多的内容。这个 AJAX 请求通常会包含一个 'page' 参数，指示应该加载哪一页的内容。
            # 如果用户已经滚动到了最后一页，并且继续滚动，那么 'page' 参数可能会超出页面的范围。在这种情况下，如果服务器端返回一个错误响应（如 404 Not Found 或 400 Bad
            # Request），可能会导致客户端的 JavaScript 代码抛出一个错误，或者在用户界面上显示一个错误消息。
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    ctx = {'section': 'images', 'images': images}
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', ctx)
    else:
        return render(request, 'images/image/list.html', ctx)
