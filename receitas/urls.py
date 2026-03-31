from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('receitas/', views.lista_receitas, name='lista_receitas'),
    path('logout/', views.logout_view, name='logout'),
    path('receitas/nova/', views.receita_create, name='receita_create'),
    path('receitas/editar/<int:id>/', views.receita_update, name='receita_update'),
    path('receitas/excluir/<int:id>/', views.receita_delete, name='receita_delete'),
]