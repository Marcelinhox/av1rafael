from django.db import models

# Create your models here.
from django.db import models

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

class Fatura(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    status = models.CharField(max_length=20)
    data_emissao_boleto = models.DateField()