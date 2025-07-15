from django.urls import path
from . import  views

urlpatterns = [
    path('get_blogs/',views.GetBlogsView.as_view(), name='get_blogs'),
    path('get_my_blog_list/', views.GetMyBlogList.as_view(), name='get_my_blog_list'),
    path('add_blog/',views.AddBlogView.as_view(), name='add_blog'),
    path('edit_blog/',views.EditBlogView.as_view(), name='edit_blog'),
    path("toggle_like/", views.ToggleLikeView.as_view(), name="toggle_like"),

]


