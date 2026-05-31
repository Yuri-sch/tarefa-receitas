from django.contrib import admin
from receitas.models import Usuario, Receita

# Registra as tabelas no painel administrativo do Django
admin.site.register(Usuario)
admin.site.register(Receita)
