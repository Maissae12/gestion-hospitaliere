from django.contrib import admin
from django.urls import path, include
from hopital import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home_dashboard/', views.home_dashboard, name='home_dashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='hopital/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='hopital/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='hopital/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='hopital/password_reset_complete.html'), name='password_reset_complete'),

    # Vues Django classiques
    path('hopital/', include('hopital.urls')),

    # API REST (Django REST Framework)
    path('api/', include('hopital.api_urls')),
    path('api-auth/', include('rest_framework.urls')),  # Login/logout DRF browsable API

    # Vue.js SPA (interface Vue)
    path('vue/', views.vue_spa, name='vue_spa'),
]
