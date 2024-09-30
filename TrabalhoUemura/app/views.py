from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect


from .backupManager import backupUsuariosCSV
from .formulario import FormularioDeLivros
from .models import Usuarios, Livros
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# ANOTAÇÕES - Guilherme
# Arquivo responsável por definir as regras de negócio do app. Vulgo ACTION.
# E onde está o html para ser exibido depois.


def checarBackUp(): # Verifica a integridade do banco de dados a partir dos backups csv
    backupUsuariosCSV.verificaIntegridadeUsuarios()

#----------------------------------------------------------------------------------------------------
#   Processo de autenticacao

def home(request):
    checarBackUp()
    return redirect('auth/login')


def cadastro(request):
    checarBackUp()
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
        backupUsuariosCSV.atualizaBackupUsuarios()
        return redirect('login')


def login_view(request):
    checarBackUp()
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    else:
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome, password=senha)
        if user is not None:
            login(request, user)
            # Armazena o URL de destino na sessão
            request.session['redirect_url'] = request.POST.get('next', reverse('meus_livros'))

            return HttpResponseRedirect(request.session['redirect_url'])
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
            return render(request, 'auth/login.html')

#----------------------------------------------------------------------------------------------------
#   Meus Livros

@login_required(login_url='/auth/login/')
def meus_livros(request):
    checarBackUp()
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    livros = Livros.objects.filter(usuarioDono=usuario)
    return render(request, 'meus_livros.html', {'livros': livros, 'usuario' : usuario})


@login_required(login_url='/auth/login/')
def dashboard(request):
    checarBackUp()
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    usuarios = Usuarios.objects.all
    livros = Livros.objects.all
    return render(request, 'dashboard.html', {'livros': livros, 'usuario' : usuario, 'usuarios' : usuarios})


@login_required(login_url='/auth/login')
def cadastrar_livro(request):
    if request.method == 'POST':
        form = FormularioDeLivros(request.POST)
        if form.is_valid():
            livro = form.save()  # Salva o livro
            # Não é necessário fazer nada aqui, o Django cuida das relações ManyToMany automaticamente
            return redirect('meus_livros')  # Redirecione para onde você quiser
    else:
        form = FormularioDeLivros()
    return render(request, 'cadastrar_livro.html', {'form': form})

@login_required(login_url='/auth/login/')
def emprestar_livro(request, id):
    usuario = get_object_or_404(Usuarios, id_usuario=request.user.id)
    livro = get_object_or_404(Livros, id=id)
    if request.method == 'POST':
        livro.usuarioDono = usuario
        livro.save()
        return redirect('dashboard')
    return render(request, 'emprestar_livro.html', {'livro': livro})


@login_required(login_url='/auth/login/')
def emprestar_livro_modal(request):
    livro_id = request.GET.get('livro_id')
    livro = get_object_or_404(Livros, id=livro_id)
    return render(request, 'emprestar_livro.html', {'livro': livro})


@login_required(login_url='/auth/login')
def editar_preco_livro(request,id):
    livro = get_object_or_404(Livros,id=id )
    if request.method == 'POST':
        form = FormularioDeLivros(request.POST, instance=Livros)
        if form.is_valid():
            form.save()
            return redirect('meus_livros')
        else:
            form = FormularioDeLivros(instance=Livros)
            return render(request, 'dashboard.html', {'form': form, 'livro': livro})