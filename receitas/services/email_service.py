from django.core.mail import send_mail
from django.conf import settings

# Envia um e-mail notificando a criação ou atualização de uma receita.
def enviar_email_notificacao_receita(receita, acao, email_destino):
    if not email_destino:
        return 
        
    assunto = f'Receita {acao}: {receita.nome}'
    mensagem = f'''Olá!

A receita "{receita.nome}" foi {acao} com sucesso no sistema.

Detalhes:
- Tipo: {receita.tipo_receita}
- Custo: R$ {receita.custo},00
- Descrição: {receita.descricao}

Atenciosamente,
Sistema de Gerenciamento de Receitas'''
    
    send_mail(
        assunto,
        mensagem,
        settings.EMAIL_HOST_USER,
        [email_destino],
        fail_silently=False,
    )