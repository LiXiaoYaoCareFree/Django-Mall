from django.urls import path
from . import views
# 设置应用命名空间
app_name = 'contents'
urlpatterns = [
    path("", views.IndexView.as_view(), name='index')
]