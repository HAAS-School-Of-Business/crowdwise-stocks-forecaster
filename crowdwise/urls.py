"""crowdwise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from question import views as q_views


urlpatterns = [
    path('', q_views.home_view),
    path('submit-vote/', q_views.vote_submit_view),

    path('questions/', q_views.question_list_view),
    path('questions/<int:question_id>', q_views.question_detail_view),
    # path('users/', include('users.urls'), name='users'),
    # path('feed/', include('feed.urls'), name='feed'),
    path('admin/', admin.site.urls),
#     path('register/', user_views.register, name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
