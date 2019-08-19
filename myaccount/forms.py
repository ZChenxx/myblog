import re

from django import forms
from django.contrib.auth.models import User

from .models import UserProfile

class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)
    telephone = forms.CharField(label='Telephone', max_length=50, required=False)


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern,email)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    email = forms.EmailField(label='邮箱')
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.ValidationError("用户名长度小于6")
        elif len(username) >50:
            raise forms.ValidationError("用户名过长")
        else:
            filter_result = User.objects.filter(username__exact=username)   #__exact 精确等于 like ‘aaa’   __iexact 精确等于 忽略大小写 ilike ‘aaa’ __contains 包含 like ‘%aaa%’ __icontains 包含 忽略大小写 ilike ‘%aaa%’
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在")

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("邮箱已存在")
        else:
            raise forms.ValidationError("请使用有效邮箱")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) <6:
            raise forms.ValidationError("密码太短")
        elif len(password1) >20:
            raise forms.ValidationError("密码过长")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不同，请确认")

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError("用户名不存在")

        return username



class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='旧密码',widget=forms.PasswordInput)
    password1 = forms.CharField(label='新密码',widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认新密码',widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 6:
            raise forms.ValidationError("密码太短")
        elif len(password1) >20:
            raise forms.ValidationError("密码太长")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError("密码不匹配")
        return password2



