from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from charity_app import views   # ✅ fixed import
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.home, name='home'),
    path('campaign/new/', views.campaign_create, name='campaign_create'),
    path('campaign/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/<int:pk>/qr/', views.campaign_qr_refresh, name='campaign_qr_refresh'),

    path('donate/<int:pk>/', views.donate, name='donate'),
    path('donation/<int:pk>/verify/', views.verify_donation, name='verify_donation'),

    path('volunteer/<int:pk>/avail/', views.volunteer_set_availability, name='volunteer_avail'),

    # ✅ include API urls from app
    path('api/', include('charity_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
