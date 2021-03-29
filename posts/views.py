from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post, PostImage

def blog_view(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts':posts})

def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'detail.html', {
        'post':post,
        'photos':photos
    })

def gallery_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'gallery-view.html', {
        'post':post,
        'photos':photos
    })

def create_post_view(request):
    if request.method == 'POST':
        length = request.POST.get('length')
        title = request.POST.get('title')
        description = request.POST.get('description')

        post = Post.objects.create(
            title=title,
            description=description
        )
        
        for file_num in range(0, int(length)):
            image = 'images%s' %(file_num)
            PostImage.objects.create(
                post=post,
                images=request.FILES.get(image)
            )


    return render(request, 'create-post.html')

def update_post_view(request):
    if request.method == 'POST':
        length = request.POST.get('length')
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        for file_num in range(0, int(length)):
            image = 'images%s' %(file_num)
            PostImage.objects.create(
                post=post,
                images=request.FILES.get(image)
            )

    url = reverse('detail', kwargs={'id': post_id})
    return HttpResponseRedirect(url)

def delete_image(request, id):
    postobj = PostImage.objects.get(pk=id)
    post_id = postobj.post_id
    if postobj.images:
        postobj.images.delete()
    image = postobj.delete()
    url = reverse('detail', kwargs={'id': post_id})
    return HttpResponseRedirect(url)
    