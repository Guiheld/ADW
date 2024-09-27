from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .backupManager import backupCSV
from .models import Tarefas, Usuarios
from .formulario import Formulario_de_tarefas
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Tarefas
from django.urls import reverse

# ANOTAÇÕES - Guilherme
# Arquivo responsável por definir as regras de negócio do app. Vulgo ACTION.
# E onde está o html para ser exibido depois.

# Create your views here.



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
        backupCSV.atualizaBackupUsuarios()
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
            request.session['redirect_url'] = request.POST.get('next', reverse('definir_tarefas'))

            return HttpResponseRedirect(request.session['redirect_url'])
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
            return render(request, 'auth/login.html')


@login_required(login_url='/auth/login/')
def dashboard(request):
    usuarios = Usuarios.objects.all()
    tarefas_por_usuario = {usuario: Tarefas.objects.filter(tarefa_atribuida=usuario) for usuario in usuarios}
    return render(request, 'dashboard.html', {'tarefas_por_usuario': tarefas_por_usuario})


#----------------------------------------------------------------------------------------------------
#config bloco de tarefas

@login_required(login_url='/auth/login/')
def definir_tarefa(request):
    redirect_url = request.session.pop('redirect_url', None) # Recupera o URL de destino da sessão se existir
    usuario_id = request.user.id
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    tarefas = Tarefas.objects.filter(tarefa_atribuida=usuario_id)
    if redirect_url:
        return HttpResponseRedirect(redirect_url)

    return render(request, 'definir_tarefa.html/', {'tarefas': tarefas, 'usuario' : usuario})


@login_required(login_url='/auth/login/')
def criar_tarefa(request):
    if request.method == 'POST':
        form = Formulario_de_tarefas(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            try:
                usuario = Usuarios.objects.get(id_usuario=request.user.id)
            except Usuarios.DoesNotExist:
                usuario = None
            tarefa.entrada_tarefa = usuario
            tarefa.save()
            return redirect('definir_tarefas')
    else:
        form = Formulario_de_tarefas(request.POST)
        # Popula o campo tarefa_atribuida com todos os usuários disponíveis
        form.fields['tarefa_atribuida'].queryset = Usuarios.objects.all()

    return render(request, 'formulario_tarefas.html', {'form': form})


@login_required(login_url='/auth/login/')
def atualizar_tarefa(request, tarefa_id):
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    tarefa = get_object_or_404(Tarefas, id=tarefa_id, tarefa_atribuida=usuario)
    if request.method == 'POST':
        form = Formulario_de_tarefas(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('definir_tarefas')
    else:
        form = Formulario_de_tarefas(instance=tarefa)

    return render(request, 'formulario_tarefas.html', {'form': form})

@login_required(login_url='/auth/login/')
def atualizar_tarefa_dashboard(request, tarefa_id):
    tarefa = get_object_or_404(Tarefas, id=tarefa_id)
    if request.method == 'POST':
        form = Formulario_de_tarefas(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('definir_tarefas')
    else:
        form = Formulario_de_tarefas(instance=tarefa)

    return render(request, 'formulario_tarefas.html', {'form': form})


@login_required(login_url='/auth/login/')
def deletar_tarefa(request, tarefa_id):
    usuario = get_object_or_404(Usuarios, id_usuario=request.user.id)
    tarefa = get_object_or_404(Tarefas, id=tarefa_id, entrada_tarefa=usuario)
    if request.method == 'POST':
        tarefa.delete()
        return redirect('dashboard')

    return render(request, 'confirmar_exclusao.html', {'tarefa': tarefa})

@login_required(login_url='/auth/login/')
def deletar_tarefa_dashboard(request, tarefa_id):
    tarefa = get_object_or_404(Tarefas, id=tarefa_id)
    if request.method == 'POST':
        tarefa.delete()
        return redirect('dashboard')

    return render(request, 'confirmar_exclusao.html', {'tarefa': tarefa})



