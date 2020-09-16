from django.urls import path,include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('create', views.CreateMessageView)
router.register('', views.MessageView)





urlpatterns = [
    path('auth/<pk>/groups/', views.show_group_member, name="show-message-members"),
    path('count/<pk>/', views.get_comment_count, name="show-message-count"),
    path('thread/<pk>/', views.get_thread, name="show-message-replies"),
    path('rest/', include('rest_framework.urls')),
    path('messages/', include(router.urls)),
    
]
