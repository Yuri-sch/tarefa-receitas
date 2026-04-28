from django.test import TestCase
from django.urls import reverse
from receitas.models import Usuario, Receita

class ReceitaViewsTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome="Admin", login="admin", senha="123", situacao="Ativo")
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

        self.receita = Receita.objects.create(
            nome="Bolo de Laranja", descricao="Bolo simples", custo=10, tipo_receita="doce"
        )

    # Teste 9: Acesso à Listagem
    def test_lista_receitas_view(self):
        response = self.client.get(reverse('lista_receitas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_receitas.html')

    # Teste 10: Acesso à interface de Criação
    def test_receita_create_get(self):
        response = self.client.get(reverse('receita_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receita_form.html')

    # Teste 11: Criação de Nova Receita
    def test_receita_create_post(self):
        dados = {'nome': 'Pudim', 'descricao': 'Pudim de leite', 'custo': 20, 'tipo_receita': 'doce'}
        response = self.client.post(reverse('receita_create'), dados)
        self.assertRedirects(response, reverse('lista_receitas'))
        # Verifica se agora existem 2 receitas no banco
        self.assertEqual(Receita.objects.count(), 2)

    # Teste 12: Acesso à interface de Edição
    def test_receita_update_get(self):
        response = self.client.get(reverse('receita_update', args=[self.receita.id]))
        self.assertEqual(response.status_code, 200)
        # Verifica se o nome da receita já vem preenchido no formulário
        self.assertContains(response, 'Bolo de Laranja')

    # Teste 13: Atualização de Receita já Existente
    def test_receita_update_post(self):
        
        dados = {'nome': 'Bolo de Laranja (Grande)', 'descricao': 'Bolo', 'custo': 15, 'tipo_receita': 'doce'}
        response = self.client.post(reverse('receita_update', args=[self.receita.id]), dados)
        self.assertRedirects(response, reverse('lista_receitas'))
        
        # Atualiza a instância com os dados da base de dados e verifica a alteração
        self.receita.refresh_from_db()
        self.assertEqual(self.receita.nome, 'Bolo de Laranja (Grande)')
        self.assertEqual(self.receita.custo, 15)

    # Teste 14: Exclusão de Receita
    def test_receita_delete_post(self):
        response = self.client.post(reverse('receita_delete', args=[self.receita.id]))
        self.assertRedirects(response, reverse('lista_receitas'))
        self.assertEqual(Receita.objects.count(), 0) # A base de dados deve estar vazia