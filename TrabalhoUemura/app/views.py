import os

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .dadosManager.analisaDados import criar_grafico, analisar_dataset
from .formulario import formulario_nova_analise
from .models import Usuarios, analise
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

# ANOTAÇÕES - Guilherme
# Arquivo responsável por definir as regras de negócio do app. Vulgo ACTION.
# E onde está o html para ser exibido depois.

# Path dos datasets
sf_salaries_path = os.path.join(settings.BASE_DIR, "app", "dadosManager", "dadosImportados", "Salaries.csv")
salary_dataset_with_extra_features_path = os.path.join(settings.BASE_DIR, "app", "dadosManager", "dadosImportados", "Salary_Dataset_with_Extra_Features.csv")
datascience_salaries_2024_path = os.path.join(settings.BASE_DIR, "app", "dadosManager", "dadosImportados", "DataScience_salaries_2024.csv")

#----------------------------------------------------------------------------------------------------
#   Processo de autenticacao

def home(request):
    return redirect('auth/login')


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'auth/cadastro.html')
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se nome de usuario já está em uso
        if Usuarios.objects.filter(nome=nome).exists():
            return HttpResponse('Nome de usuário já existente')

        # Cria e salva o novo usuário
        senha_hash = make_password(senha)  # Hash da senha
        user = Usuarios(nome=nome, email=email, senha=senha_hash) # cadastra modelo personalizado do models
        user.save()
        user_django = User(username=nome, email=email) # cadastra user padrao do django
        user_django.set_password(senha)
        user_django.save()
        return redirect('login')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    else:
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome, password=senha)
        if user is not None:
            login(request, user)
            # Armazena o URL de destino na sessão
            request.session['redirect_url'] = request.POST.get('next', reverse('minhas_analises'))
            return HttpResponseRedirect(request.session['redirect_url'])
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
            return render(request, 'auth/login.html')

#----------------------------------------------------------------------------------------------------
# Paginas Principais

@login_required(login_url='/auth/login/')
def minhas_analises(request):
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    analises = analise.objects.filter(id_usuario_autor=usuario.id_usuario)
    return render(request, 'minhas_analises.html', {'usuario' : usuario, 'analises' : analises})


@login_required(login_url='/auth/login/')
def dashboard(request):
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    usuarios = Usuarios.objects.all
    analises = analise.objects.all
    return render(request, 'dashboard.html', {'usuario' : usuario, 'usuarios' : usuarios, 'analises' : analises})

#----------------------------------------------------------------------------------------------------
# Operacoes

@login_required(login_url='/auth/login/')
def nova_analise(request):
    if request.method == 'POST':
        form = formulario_nova_analise(request.POST)
        if form.is_valid():
            analise = form.save(commit=False)
            analise.id_usuario_autor = Usuarios.objects.get(id_usuario=request.user.id)
            if analise.nome_analise == 'SF_Salaries':
                analise.path_arquivo = sf_salaries_path
                analise.save()
                return redirect('minhas_analises')
            elif analise.nome_analise == 'Salary_Dataset_with_Extra_Features':
                analise.path_arquivo = salary_dataset_with_extra_features_path
                analise.save()
                return redirect('minhas_analises')
            elif analise.nome_analise == 'DataScience_salaries_2024':
                analise.path_arquivo = datascience_salaries_2024_path
                analise.save()
                return redirect('minhas_analises')
    else:
        form = formulario_nova_analise()
    return render(request, 'nova_analise.html', {'form': form})


@login_required(login_url='/auth/login/')
def analisar_dado(request, id):
    if id >= 0:
        try:
            analise_obj = analise.objects.get(id_analise=id)
            df = analisar_dataset(analise_obj)
            if df is not None:
                graficos_html = criar_grafico(df)
                return render(request, 'visualizar_analise.html', {'graficos_html': graficos_html, 'analise_obj' : analise_obj})
        except analise.DoesNotExist:
            return HttpResponse("Análise não encontrada", status=404)
        except Exception as e:  # Captura outras exceções
            return HttpResponse("Ocorreu um erro ao processar a análise", status=500)
    return HttpResponse("ID inválido", status=400)