from django.shortcuts import redirect
from receitas.models import Receita
from receitas.services.relatorio_service import gerar_pdf_receitas

def exportar_pdf(request):
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

    nome_usuario = request.session.get('usuario_nome')
    
    return gerar_pdf_receitas(receitas, nome_usuario)