"""crowdpredictiveanalytics URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from typing import Protocol
from django.contrib import admin
from django.urls import path, include
from question import views as q_views
from accounts import views as a_views
from django.conf import settings
from django.conf.urls.static import static
from question.models import Question
from django.contrib.sitemaps import GenericSitemap # new
from django.contrib.sitemaps.views import sitemap # new
from question.views import (home_view, question_list_view, vote_submit_view)
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.site.site_header="Crowd Predictive Analytics Admin"

handler404 = 'crowdpredictiveanalytics.views.custom_page_not_found_view'
handler500 = 'crowdpredictiveanalytics.views.custom_error_view'
# handler403 = 'crowdpredictiveanalytics.views.custom_page_not_found_view'
# handler400 = 'crowdpredictiveanalytics.views.custom_page_not_found_view'

from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', include('question.urls', namespace='question')),
    path('register/', a_views.accounts_register, name='register'),
    path('submit-vote/', q_views.vote_submit_view),
    path('submit-vote', q_views.vote_submit_view),
    path('questions/', q_views.question_list_view),
    path('questions/<int:question_id>', q_views.vote_single),
    path('profile/', a_views.profile, name='profile'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
#     path('register/', user_views.register, name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
