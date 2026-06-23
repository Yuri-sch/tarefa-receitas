import math

from django.db import models

class Categoria(models.Model):
    descricao = models.CharField(max_length=100)

    class Meta:
        db_table = 'categoria'
        app_label = 'receitas'

    def __str__(self):
        return self.descricao