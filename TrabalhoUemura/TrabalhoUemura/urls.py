"""
URL configuration for TrabalhoUemura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

# ANOTAÇÕES - Guilherme
# Arquivo para armazenar as rotas que serão utilizadas no projeto. Este arquivo -
# armazenará as rotas do projeto em geral

from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # urls de auth
    #--------------------------------------------
    path('', views.home, name='home'),
    path('auth/cadastro/', views.cadastro, name='cadastro'),
    path('auth/login/', views.login_view, name='login'),
    #--------------------------------------------
    path('minhas_analises/', views.minhas_analises, name='minhas_analises'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #--------------------------------------------
    path('nova_analise/', views.nova_analise, name='nova_analise'),
    path('analisar/<int:id>', views.analisar_dado, name='analisar'),

    ]
