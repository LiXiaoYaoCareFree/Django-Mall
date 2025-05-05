from django.urls import path, re_path
from . import views

# 设置应用命名空间
app_name = 'users'
urlpatterns = [
    # 用户注册
    path('register/', views.RegisterView.as_view(), name='register'),
]