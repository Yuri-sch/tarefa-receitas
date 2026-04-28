# receitas/urls.py
from django.urls import path
from receitas.views import auth_views, receita_views, relatorio_views

urlpatterns = [
    # Rotas de Autenticação
    path('', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Rotas de Receitas (CRUD e Listagem)
    path('receitas/', receita_views.lista_receitas, name='lista_receitas'),
    path('receitas/nova/', receita_views.receita_create, name='receita_create'),
    path('receitas/editar/<int:id>/', receita_views.receita_update, name='receita_update'),
    path('receitas/excluir/<int:id>/', receita_views.receita_delete, name='receita_delete'),
    
    # Rotas de Relatórios
    path('receitas/exportar-pdf/', relatorio_views.exportar_pdf, name='exportar_pdf'),
]