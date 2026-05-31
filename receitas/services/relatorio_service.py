from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def gerar_pdf_receitas(receitas, nome_usuario):
    contexto = {
        'receitas': receitas,
        'nome_usuario': nome_usuario
    }

    template = get_template('receitas_pdf.html')
    html = template.render(contexto)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_receitas.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Tivemos alguns erros ao gerar o PDF', status=500)
    
    return response