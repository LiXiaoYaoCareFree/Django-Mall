import re
from django.db import DatabaseError
from .models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views import View
import logging

logger = logging.getLogger('django')

class RegisterView(View):
    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')
    def post(self, request):
        # 1.接收请求参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        # 2.校验参数
        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个字符
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20个字符的密码')
        # 判断两次密码是否一致
        if password != password2:
            return HttpResponseForbidden('两次密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入合法的手机号')
        # 判断是否同意协议
        if allow != 'on':
            return HttpResponseForbidden('请同意协议')
        # 3. 保存注册数据
        try:
            User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            # 返回注册结果
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        return redirect(reverse('contents:index'))
