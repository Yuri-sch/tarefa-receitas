from django.shortcuts import render, redirect
from django.contrib import messages
from receitas.models import Usuario

def login_view(request):
    if request.session.get('usuario_id'):
        return redirect('lista_receitas')

    if request.method == 'POST':
        login_form = request.POST.get('login')
        senha_form = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(login=login_form, senha=senha_form)
            
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nome'] = usuario.nome
            request.session['usuario_email'] = usuario.email 
            
            return redirect('lista_receitas')
            
        except Usuario.DoesNotExist:
            messages.error(request, 'Login ou senha inválidos.')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')