from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, UserProfileEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegisterForm
    temp = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class()
        return render(request, self.temp, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username= cd['username'], password= cd['password1'], email= cd['email'])
            messages.success(request, 'You registred successfully', 'success')
            return redirect('home:home')
        return render(request, self.temp, {'form':form})


class UserLoginView(View):
    form_class = UserLoginForm
    temp = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class()
        return render(request, self.temp, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in ', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.temp, {'form': form})
    

class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successful', 'success')
        return redirect('home:home')
    

class UserProfileView(LoginRequiredMixin, View):
    temp = 'account/profile.html'
    
    def get(self, request, user_id):
        user = get_object_or_404(User, pk = user_id)
        posts = user.posts.all()
        is_following = False 
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            is_following = True
        return render(request, self.temp, {'user': user, 'posts':posts, 'is_following': is_following})
    

class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            messages.error(request, f'you already have followed {user.username}', 'danger')
        else : 
            Relation.objects.create(from_user = request.user, to_user = user)
            messages.success(request, f'you follow {user.username}, successfully', 'success')
        return redirect('account:profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk = user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f'you unfollow {user.username}', 'success')
        else: 
            messages.error(request, f'you don`t have {user.username} follow!', 'danger')
        return redirect('account:profile', user.id)



class UserEditProfileView(View):
    form_class = UserProfileEditForm
    temp = 'account/edit_profile.html'
    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email, 'username': request.user.username})
        return render(request, self.temp, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST, instance= request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.username = form.cleaned_data['username']
            request.user.save()
            messages.success(request, 'You Update your profile successfully', 'success')
            return redirect('account:profile', request.user.id)