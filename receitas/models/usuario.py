from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    senha = models.CharField(max_length=120)
    email = models.EmailField(max_length=150, null=True, blank=True)
    situacao = models.CharField(max_length=20)

    class Meta:
        db_table = 'usuario'
        app_label = 'receitas' # Ajuda o Django a mapear o model

    def __str__(self):
        return self.nome