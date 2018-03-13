# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_comments
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django_comments.forms import CommentDetailsForm

from models import BBS, BBS_user, Category, Profile


#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())


class ProfileForm(forms.Form):
    name = forms.CharField(max_length = 100)
    picture = forms.ImageField()
''''
    def clean_message(self):
        username = self.cleaned_data.get("username")
        print(username)
        return username
'''


#  注册
@csrf_protect
def register(req):
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #添加到数据库
            User.objects.create(username= username,password=password)
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render(req, 'app01/register.html', context={'form':form}, )

#  登录
# @csrf_protect  #  加了middlemine，可有可无
# @csrf_exempt   #  禁用csrf保护机制
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            # user = User.objects.filter(username__exact = username,password__exact = password)
            user = auth.authenticate(username=username, password=password)
            if user:
                #比较成功，跳转index
                # response = HttpResponseRedirect('/')
                # #将username写入浏览器cookie,失效时间为3600
                # response.set_cookie('username',username,3600)
                # return response
                auth.login(req, user)
                req.session['username'] = username
                return HttpResponseRedirect('/')

            else:
                #比较失败，还在login
                return render(req, 'app01/login.html')
    else:
        return render(req, 'app01/login.html',  context={'login_err':'Wrong username or password!'},)

# 登录成功
@csrf_protect
def index(request):
    bbs_list = BBS.objects.all()
    category_list = Category.objects.all()
    return render(request, 'app01/index.html', context={
        'bbs_list': bbs_list,
        'category_list': category_list,
        # 'category_id': 0,
        # 'user': request.user,
        # 'bbs_pub': 1,
    })

#  退出
@csrf_protect
def logout(request):
    user = request.user
    #清理cookie里保存username
    auth.logout(request)
    return HttpResponse("<b>%s</b> 退出! <br/><a href='/login/'>重新登录</a>" % user)

@csrf_protect
def detail(request, bbs_id):
    bbs = BBS.objects.get(id=bbs_id)
    category_list = Category.objects.all()
    return render(request, 'app01/bbs_detail.html', context={
        'bbs_obj': bbs,
        'category_list': category_list,
        # 'user': request.user,

    })

@csrf_protect
def sub_comment(request):
    # print request.POST
    # print request.user
    bbs_id = request.POST.get('bbs_id')
    comment = request.POST.get('comment_content')

    # django_comments.forms
    # CommentDetailsForm.as_p()
    django_comments.models.Comment.objects.create(
            content_type_id = 7,
            object_pk = bbs_id,
            site_id = 1,
            user = request.user,
            comment = comment,
                                   )


    return HttpResponseRedirect('/detail/%s' % bbs_id)
    # return render(request, 'app01/detail.html')
@csrf_protect
def bbs_pub(request):
    category_list = Category.objects.all()
    return render(request, 'app01/bbs_pub.html', {'category_list': category_list})

@csrf_protect
def bbs_sub(request):
    print request.POST
    # print BBS_user.objects.all()
    # print BBS.objects.all()
    # print Category.objects.all()

    bbs_id = request.POST.get('bbs_id')
    author = BBS_user.objects.get(user__username=request.user)
    bbs_category = request.POST.get('bbs_category')
    # category=Category.objects.get(name=bbs_category),
    print request.POST.get('bbs__id')  # >>>>>None
    print request.POST.get('bbs__category')  # >>>>>None
    # BBS.objects.create(
    #     title = '暂定标题',
    #     content = request.POST.get('content'),
    #     summury = '爱互动哈',
    #     category=Category.objects.get(name=category_select),
    #
    #     # category = 'China',
    #     author = author,
    #     ranking = 1,
    #     view_count = 1,
    # )
    return HttpResponse('yes')

def category(request, cate_id):
    bbs_list = BBS.objects.filter(category__id = cate_id)
    category_list = Category.objects.all()
    return render(request, 'app01/index.html', context={
        'bbs_list': bbs_list,
        'category_list': category_list,
        'category_id': int(cate_id),

    })


def SaveProfile(request):
    saved = False

    if request.method == "POST":
        # Get the posted form
        MyProfileForm = ProfileForm(request.POST, request.FILES)

        if MyProfileForm.is_valid():
            print("--------------------")
            profile = Profile()
            profile.name = MyProfileForm.cleaned_data["name"]
            profile.picture = MyProfileForm.cleaned_data["picture"]
            profile.save()
            saved = True
    else:
        MyProfileForm = ProfileForm()

    return render(request, 'app01/saved.html', locals())
# Create your views here.
