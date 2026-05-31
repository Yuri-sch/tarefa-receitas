from django.db import models

class Receita(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150)
    data_registro = models.DateField(auto_now_add=True)
    custo = models.IntegerField()
    tipo_receita = models.CharField(max_length=45)

    class Meta:
        db_table = 'receita'
        app_label = 'receitas'

    def __str__(self):
        return f"{self.nome} ({self.tipo_receita})"