from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm #add this

from .models import Post, PostImage

def blog_view(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts':posts})

def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    if request.user.is_authenticated:
        return render(request, 'gallery-view.html', {
            'post':post,
            'photos':photos
        })
    else:
        return render(request, 'detail.html', {
        'post':post,
        'photos':photos
        })

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

@login_required
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
    