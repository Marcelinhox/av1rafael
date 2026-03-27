from django.test import TestCase
from .models import Cliente, Fatura
from datetime import date

class BillingSystemTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com",
            telefone="11999999999",
            endereco="Rua Teste, 100"
        )
        self.fatura = Fatura.objects.create(
            cliente=self.cliente,
            valor=150.50,
            data_vencimento=date(2025, 12, 31)
        )

    def test_cliente_criado(self):
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(self.cliente.nome, "João Silva")

    def test_fatura_criada(self):
        self.assertEqual(Fatura.objects.count(), 1)
        self.assertEqual(self.fatura.valor, 150.50)
        self.assertEqual(self.fatura.status, "pendente")

    def test_view_cadastro(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TechSolutions Ltda")

    def test_view_listagem(self):
        response = self.client.get('/faturas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "João Silva")
        # Django l10n formats with comma in pt-br
        self.assertContains(response, "150,50")
