from django.shortcuts import render, redirect, get_object_or_404
from receitas.models import Usuario, Receita
from receitas.forms import ReceitaForm
from receitas.services.email_service import enviar_email_notificacao_receita

def lista_receitas(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    receitas = Receita.objects.all()
    
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()
    tipo = request.GET.get('tipo_receita', '').strip()

    if data_inicio:
        receitas = receitas.filter(data_registro__gte=data_inicio)
    if data_fim:
        receitas = receitas.filter(data_registro__lte=data_fim)
    if tipo:
        receitas = receitas.filter(tipo_receita__icontains=tipo)
    
    contexto = {
        'receitas': receitas,
        'nome_usuario': request.session.get('usuario_nome'),
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'tipo_receita': tipo,
        }
    }
    
    return render(request, 'lista_receitas.html', contexto)

def receita_create(request):
    if not request.session.get('usuario_id'): return redirect('login')
    
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            nova_receita = form.save()
            
            email_usuario = request.session.get('usuario_email')
            if not email_usuario: 
                usuario = Usuario.objects.get(id=request.session.get('usuario_id'))
                email_usuario = usuario.email
                
            enviar_email_notificacao_receita(nova_receita, 'CRIADA', email_usuario)
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
            receita_atualizada = form.save()
            usuario = Usuario.objects.get(id=request.session.get('usuario_id'))
            
            enviar_email_notificacao_receita(receita_atualizada, 'ATUALIZADA', usuario.email)
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