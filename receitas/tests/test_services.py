from django.test import TestCase
from unittest.mock import patch
from receitas.models import Receita
from receitas.services.email_service import enviar_email_notificacao_receita
from django.urls import reverse
from receitas.models import Usuario

class ServicesTest(TestCase):
    def setUp(self):
        self.receita = Receita.objects.create(
            nome="Empada", descricao="Massa podre", custo=8, tipo_receita="salgada"
        )
        self.usuario = Usuario.objects.create(nome="Admin", login="admin", senha="123")

    # Teste 18: Testar Serviço de E-mail com Mock
    @patch('receitas.services.email_service.send_mail')
    def test_enviar_email_notificacao(self, mock_send_mail):
        enviar_email_notificacao_receita(self.receita, 'CRIADA', 'teste@exemplo.pt')
        
        # Verifica se a função nativa do Django foi chamada pelo menos uma vez pelo nosso serviço
        self.assertTrue(mock_send_mail.called)
        
        # Verifica se os argumentos estão corretos (destinatário)
        args, kwargs = mock_send_mail.call_args
        self.assertIn('teste@exemplo.pt', args[3]) # O 4º argumento do send_mail é a lista de destinatários

    # Teste 19: Testar Geração de PDF
    def test_gerar_pdf_receitas(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session['usuario_nome'] = self.usuario.nome
        session.save()

        response = self.client.get(reverse('exportar_pdf'))
        self.assertEqual(response.status_code, 200)
        # Verifica se o arquivo devolvido é efetivamente um PDF
        self.assertEqual(response['Content-Type'], 'application/pdf')