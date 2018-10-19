from django import forms
from django.contrib import auth

from django.forms import ModelForm
from axf.models import User

# 表单类
class LoginForm(forms.Form):
    # username = forms.CharField(max_length=12, min_length=6, required=True, \
    #                            error_messages={"required": "用户帐号不能为空", "invalid":"格式错误"}\
    #                            ,widget=forms.TextInput(attrs={"class":"c"}))
    # passwd = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput)
    #
    # verifycode = forms.CharField(max_length=4, min_length=4, required=True, widget=forms.TextInput)


    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}) )
    # verifycode = forms.CharField(label="验证码")

    # def clean(self):
    #     username = self.cleaned_data["username"]
    #     password = self.cleaned_data["password"]
    #     print(username, password)
    #
    #     user = auth.authenticate(username=username, password=password)
    #     print(user)
    #     if user is None:
    #         raise forms.ValidationError('用户名或密码错误')
    #     else:
    #         self.cleaned_data['user'] = user
    #     return self.cleaned_data












class registerForm(forms.Form):
    pass