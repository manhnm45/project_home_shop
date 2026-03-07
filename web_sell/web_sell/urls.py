"""
URL configuration for web_sell project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_home, name='home'),
    path('ai_search/', views.render_ai_search, name='ai_search'),
    path('upload_item/', views.upload_item, name='upload_item'),
    path('get_latest_result/', views.get_latest_result, name='get_latest_result'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('create_item/', views.create_item, name='create_item'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
