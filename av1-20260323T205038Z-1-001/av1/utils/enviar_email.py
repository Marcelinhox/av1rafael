import os
from django.conf import settings
from django.core.mail import EmailMessage
from core.models import Cliente, Fatura


def enviar_emails():

    print("Iniciando envio de emails...")

    clientes = Cliente.objects.all()

    for cliente in clientes:

        faturas = Fatura.objects.filter(cliente=cliente)

        if not faturas.exists():
            print(f"Cliente {cliente.cpf} sem faturas.")
            continue

        for fatura in faturas:

            assunto = f"Fatura TechSolutions - Vencimento {fatura.data_vencimento}"

            mensagem = f"""
Olá {cliente.nome},

Sua fatura está disponível.

Valor: R$ {fatura.valor}
Vencimento: {fatura.data_vencimento}

Atenciosamente,
TechSolutions
"""

            # caminho do PDF
            caminho_pdf = os.path.join(
                settings.BASE_DIR,
                'rpa',
                'boletos',
                f"fatura_{cliente.cpf}_{fatura.id}.pdf"
            )

            email = EmailMessage(
                assunto,
                mensagem,
                settings.EMAIL_HOST_USER,
                ['marcelo.marq2001@gmail.com'] 
            )

            # anexa PDF se existir
            if os.path.exists(caminho_pdf):
                email.attach_file(caminho_pdf)
            else:
                print(f"PDF não encontrado: {caminho_pdf}")

            try:
                email.send()
                print(f"Email enviado para {cliente.nome}")

            except Exception as e:
                print(f"Erro ao enviar para {cliente.nome}: {e}")

                # 👇 AQUI QUE VOCÊ COLOCA
                with open('erros_email.csv', 'a') as f:
                    f.write(f"{cliente.cpf},{e}\n")

    print("Envio finalizado!")