from datetime import date
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_config.settings')
django.setup()

from receitas.models import Receita, Usuario # noqa: E402

print("Verificando/Inserindo Usuário admin...")
usuario, criado = Usuario.objects.get_or_create(
    login='admin',
    defaults={
        'nome': 'Administrador',
        'senha': 'senha123',
        'email': 'yurischaffer028@gmail.com',
        'situacao': 'Ativo',
    },
)
if criado:
    print("Usuário admin criado no PostgreSQL!")

print("Verificando/Inserindo 10 Receitas...")
hoje = date.today()

lista_receitas = [
    {
        'nome': 'Bolo de Cenoura',
        'descricao': 'Bolo fofinho com cobertura de chocolate.',
        'custo': 15,
        'tipo': 'doce',
    },
    {
        'nome': 'Coxinha de Frango',
        'descricao': 'Massa de batata com recheio cremoso.',
        'custo': 5,
        'tipo': 'salgada',
    },
    {
        'nome': 'Brigadeiro',
        'descricao': 'Docinho tradicional de leite condensado.',
        'custo': 2,
        'tipo': 'doce',
    },
    {
        'nome': 'Torta de Frango',
        'descricao': 'Torta salgada de liquidificador.',
        'custo': 25,
        'tipo': 'salgada',
    },
    {
        'nome': 'Pudim de Leite',
        'descricao': 'Pudim sem furinhos com calda.',
        'custo': 12,
        'tipo': 'doce',
    },
    {
        'nome': 'Empadão de Palmito',
        'descricao': 'Massa podre que derrete na boca.',
        'custo': 30,
        'tipo': 'salgada',
    },
    {
        'nome': 'Beijinho',
        'descricao': 'Docinho de coco ralado e cravo.',
        'custo': 2,
        'tipo': 'doce',
    },
    {
        'nome': 'Kibe Frito',
        'descricao': 'Kibe tradicional temperado com hortelã.',
        'custo': 6,
        'tipo': 'salgada',
    },
    {
        'nome': 'Torta de Limão',
        'descricao': 'Massa com creme de limão e merengue.',
        'custo': 22,
        'tipo': 'doce',
    },
    {
        'nome': 'Esfiha de Carne',
        'descricao': 'Massa macia com carne moída.',
        'custo': 4,
        'tipo': 'salgada',
    },
]

for item in lista_receitas:
    Receita.objects.get_or_create(
        nome=item['nome'],
        defaults={
            'descricao': item['descricao'],
            'data_registro': hoje,
            'custo': item['custo'],
            'tipo_receita': item['tipo'],
        },
    )

print("Banco PostgreSQL populado com sucesso!")