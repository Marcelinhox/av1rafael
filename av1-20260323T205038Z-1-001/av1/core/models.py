from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField(blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True)
    data_cadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Fatura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    status = models.CharField(max_length=20, default='pendente')
    data_emissao = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Fatura {self.id} - {self.cliente.nome}"
