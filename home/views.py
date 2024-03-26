from typing import Any
from django.http import HttpRequest
from django.shortcuts import render, redirect , get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm, CommentCreateForm , CommentReplayForm, PostSearchForm
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

class HomePageView(View):
    form_class = PostSearchForm
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = Post.objects.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': self.form_class})
    

class PostView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplayForm
    temp = 'home/post.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        can_like = False 
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, self.temp, {'posts': self.post_instance, 'comments': comments, 'form': self.form_class, 'reply_form': self.form_class_reply, 'can_like': can_like})
    

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'You submit a comment', 'success')
            return redirect('home:post', self.post_instance.id, self.post_instance.slug)
    

class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request, post_id):
        post = get_object_or_404(Post,pk = post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'You delete your post', 'success')
            return redirect('home:home')
        messages.error(request, 'You are not the author', 'danger')
        return redirect('home:home')
    

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    temp = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk = kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if request.user.id != post.user.id:
            messages.error(request, 'you can`t change this post', 'danger') 
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance= post)
        return render(request, self.temp, {'form':form})
    
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST , instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you update your post successfully', 'success')
            return redirect('home:post', post.id , new_post.slug)
        

class PostCreateView(View):
    form_class = PostCreateUpdateForm
    temp = 'home/create.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.temp, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post =form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'You craeted the Post', 'success')
            return redirect('home:post', new_post.id, new_post.slug)
        
class CommentReplyView(View):
    form_class = CommentReplayForm
    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk = post_id)
        comment = get_object_or_404(Comment, pk = comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post 
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'comment submitted', 'success')
        return redirect('home:post', post.id, post.slug)
    

class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            messages.success(request, 'you dislike this post', 'success')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'you like this post', 'success')
        return redirect('home:post', post.id, post.slug)