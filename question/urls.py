from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from accounts import views as a_views

app_name = 'question'

urlpatterns = [
    path('', views.home_view, name='homepage'),
    path('admin/', admin.site.urls),
    path('<slug:question>/', views.vote_single, name='vote_single')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)