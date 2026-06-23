from django.test import TestCase
from django.urls import reverse
from receitas.models import Usuario

class AuthTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="Administrador Teste",
            login="admin",
            senha="senha_super_secreta",
            situacao="Ativo"
        )
        self.login_url = reverse('login')
        self.lista_url = reverse('lista_receitas')
        self.logout_url = reverse('logout')

    # Teste 5: Acesso Negado
    def test_acesso_negado_sem_login(self):
        response = self.client.get(self.lista_url)
        # Deve redirecionar (HTTP 302) para a tela de login
        self.assertRedirects(response, self.login_url)

    # Teste 6: Login com Sucesso
    def test_login_com_sucesso(self):
        response = self.client.post(self.login_url, {
            'login': 'admin',
            'senha': 'senha_super_secreta'
        })
        self.assertRedirects(response, self.lista_url)
        # Verifica se a sessão foi preenchida com o ID correto
        self.assertEqual(self.client.session.get('usuario_id'), self.usuario.id)

    # Teste 7: Login Falho (senha incorreta)
    def test_login_falho(self):
        response = self.client.post(self.login_url, {
            'login': 'admin',
            'senha': 'senha_errada'
        })
        # Deve manter-se na tela de login (HTTP 200) e não iniciar sessão
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn('usuario_id', self.client.session)

    # Teste 8: Logout
    def test_logout(self):
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()
        
        response = self.client.get(self.logout_url)
        
        self.assertRedirects(response, self.login_url)
        # A sessão deve ter sido limpa
        self.assertNotIn('usuario_id', self.client.session)

    # Teste 9: A Prova dos Nove (Falha Proposital de Suíte)
    def test_travar_esteira_com_matematica_absurda(self):
        self.assertEqual(
            1 + 1, 
            5, 
        )