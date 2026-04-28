from django.test import TestCase
from receitas.models import Usuario, Receita

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="Administrador",
            login="admin",
            senha="adminpassword",
            email="admin@exemplo.pt",
            situacao="Ativo"
        )

    # Teste 1: Criação de Usuário
    def test_criacao_usuario(self):
        
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(self.usuario.nome, "Administrador")
        self.assertEqual(self.usuario.email, "admin@exemplo.pt")

    # Teste 2: Representação em String (usuário)
    def test_representacao_string_usuario(self):
        self.assertEqual(str(self.usuario), "Administrador")


class ReceitaModelTest(TestCase):
    def setUp(self):
        self.receita = Receita.objects.create(
            nome="Bolo de Cenoura",
            descricao="Bolo clássico com cobertura de chocolate",
            custo=15,
            tipo_receita="doce"
        )

    # Teste 3: Criação de Receita
    def test_criacao_receita(self):
        self.assertEqual(Receita.objects.count(), 1)
        self.assertEqual(self.receita.custo, 15)
        self.assertEqual(self.receita.tipo_receita, "doce")

    # Teste 4: Representação em String (Receita)
    def test_representacao_string_receita(self):
        self.assertEqual(str(self.receita), "Bolo de Cenoura (doce)")