from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Receita
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Receita
from .forms import ReceitaForm 
from django.contrib import messages

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
            
            return redirect('lista_receitas')
            
        except Usuario.DoesNotExist:
            messages.error(request, 'Login ou senha inválidos.')

    return render(request, 'login.html')

def lista_receitas(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    receitas = Receita.objects.all()
    
    contexto = {
        'receitas': receitas,
        'nome_usuario': request.session.get('usuario_nome')
    }
    
    return render(request, 'lista_receitas.html', contexto)

def receita_create(request):
    if not request.session.get('usuario_id'): return redirect('login')
    
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm()
    
    return render(request, 'receita_form.html', {'form': form, 'acao': 'Nova'})

def receita_update(request, id):
    if not request.session.get('usuario_id'): return redirect('login')
    
    receita = get_object_or_404(Receita, id=id)
    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(instance=receita)
        
    return render(request, 'receita_form.html', {'form': form, 'acao': 'Editar'})

def receita_delete(request, id):
    if not request.session.get('usuario_id'): return redirect('login')
    
    receita = get_object_or_404(Receita, id=id)
    if request.method == 'POST':
        receita.delete()
        return redirect('lista_receitas')
        
    return render(request, 'receita_confirm_delete.html', {'receita': receita})

def logout_view(request):
    request.session.flush()
    return redirect('login')
