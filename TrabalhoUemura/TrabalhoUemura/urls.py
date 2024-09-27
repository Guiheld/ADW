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
    path('', views.home, name='home'),
    path('auth/cadastro/', views.cadastro, name='cadastro'),
    path('auth/login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tarefas/', views.definir_tarefa, name='definir_tarefas'),
    path('tarefas/criar/', views.criar_tarefa, name='criar_tarefa'),
    path('tarefas/atualizar/<int:tarefa_id>/', views.atualizar_tarefa, name='atualizar_tarefa'),
    path('tarefas/deletar/<int:tarefa_id>/', views.deletar_tarefa, name='deletar_tarefa'),
    path('dashboard/tarefas/atualizar/<int:tarefa_id>/', views.atualizar_tarefa_dashboard, name='atualizar_tarefa_dashboard'),
    path('dashboard/tarefas/deletar/<int:tarefa_id>/', views.deletar_tarefa_dashboard, name='deletar_tarefa_dashboard'),
]
