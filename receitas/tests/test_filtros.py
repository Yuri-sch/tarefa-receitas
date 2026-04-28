from django.test import TestCase
from django.urls import reverse
from receitas.models import Usuario, Receita

class FiltrosTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome="Admin", login="admin", senha="123")
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

        # Criadas duas receitas diferentes para testar os filtros
        Receita.objects.create(nome="Coxinha", descricao="Salgado", custo=5, tipo_receita="salgada")
        Receita.objects.create(nome="Brigadeiro", descricao="Doce", custo=2, tipo_receita="doce")

    # Teste 15: Filtro por Tipo de Receita
    def test_filtro_tipo_receita(self):
        response = self.client.get(reverse('lista_receitas'), {'tipo_receita': 'doce'})
        self.assertEqual(response.status_code, 200)
        # Deve mostrar o Brigadeiro, mas não a Coxinha
        self.assertContains(response, "Brigadeiro")
        self.assertNotContains(response, "Coxinha")

    # Teste 16: Filtro por Data Início (simulando uma data do passado)
    def test_filtro_data_inicio(self):
        response = self.client.get(reverse('lista_receitas'), {'data_inicio': '2020-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Coxinha")
        self.assertContains(response, "Brigadeiro")

    # Teste 17: Filtro por Data Fim (simulando uma data antes da criação das receitas)
    def test_filtro_data_fim(self):
        response = self.client.get(reverse('lista_receitas'), {'data_fim': '2000-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Coxinha")
        self.assertNotContains(response, "Brigadeiro")