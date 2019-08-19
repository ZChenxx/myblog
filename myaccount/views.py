from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.urls import reverse

from myaccount.forms import RegistrationForm, LoginForm, ProfileForm,PwdChangeForm
from myaccount.models import UserProfile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create(username=username,password=password,email=email)

            user_profile = UserProfile(user=user)

            user_profile.save()

            return HttpResponseRedirect("/accounts/login/")
    else:
        form = RegistrationForm()

    return render(request,'account/registration.html',{'form':form})

# 当用户通过POST方法提交表单，我们先验证表单RegistrationForm的数据是否有效。如果有效，我们先用Django User模型自带的create_user方法创建user对象，再创建user_profile。用户通过一张表单提交数据，我们实际上分别存储在两张表里。
#
# 如果用户注册成功，我们通过HttpResponseRedirect方法转到登陆页面
#
# 如果用户没有提交表单或不是通过POST方法提交表单，我们转到注册页面，生成一张空的RegistrationForm
#
#


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('myaccount:profile'))

            else:
                return render(request,'account/login.html',{'form':form,'message':'密码错误'})

    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})


# 当用户通过POST方法提交表单，我们先验证表单LoginForm的数据是否有效。如果有效，我们调用Django自带的auth.authenticate() 来验证用户名和密码是否正确。如果正确且用户是活跃的，我们调用auth.login()来进行登录。
#
# 如果用户登录失败，会重新转到登录页面，并返回错误信息。
#
# 如果用户登录成功，我们通过HttpResponseRedirect方法转到用户个人信息页面
#
# 如果用户没有提交表单或不是通过POST方法提交表单，我们转到登录页面，生成一张空的LoginForm






#
@login_required
def profile(request):
    # https://www.cnblogs.com/wuchenggong/p/9675017.html
    user = request.user

    return render(request,'account/profile.html',{'user':user})
#
@login_required
def profile_update(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile,user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('myaccount:profile'))
    else:
        default_data = {'first_name':user.first_name,'last_name':user.last_name,
                        'org':user_profile.org,'telephone':user_profile.telephone,}
        form = ProfileForm(default_data)
    return render(request,'account/profile_update.html',{'form':form,'user':user})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")

@login_required
def pwd_change(request):
    user = request.user
    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username,password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/accounts/login/")

            else:
                return render(request,'account/pwd_change.html',{'form':form,'message':'旧密码错误'})
    else:
        form = PwdChangeForm()
    return render(request,'account/pwd_change.html',{'form':form})

