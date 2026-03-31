from django.db import models

class Usuario(models.Model):
    # id INT (Criado automaticamente)
    nome = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    senha = models.CharField(max_length=120)
    situacao = models.CharField(max_length=20)

    class Meta:
        db_table = 'usuario' # Força o nome exato da tabela no banco

    def __str__(self):
        return self.nome

class Receita(models.Model):
    # id INT (Criado automaticamente)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150)
    data_registro = models.DateField(auto_now_add=True)
    custo = models.IntegerField()
    tipo_receita = models.CharField(max_length=45)

    class Meta:
        db_table = 'receita' # Força o nome exato da tabela no banco

    def __str__(self):
        return f"{self.nome} ({self.tipo_receita})"