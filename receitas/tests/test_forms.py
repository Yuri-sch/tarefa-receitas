from django.test import TestCase
from receitas.forms import ReceitaForm

class ReceitaFormTest(TestCase):
    # Teste 20: Validação de Formulário (Tentando guardar uma receita sem o custo)
    def test_receita_form_invalido(self):
        dados_incompletos = {
            'nome': 'Biscoito',
            'descricao': 'Biscoito doce',
            'tipo_receita': 'doce'
            # Falta o 'custo' propositadamente
        }
        form = ReceitaForm(data=dados_incompletos)
        
        # O formulário não deve ser válido
        self.assertFalse(form.is_valid())
        # Deve ser encontrado um erro no campo 'custo'
        self.assertIn('custo', form.errors)