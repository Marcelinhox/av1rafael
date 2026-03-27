import os
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime

def registrar_log_email(fatura, status, erro=""):
    caminho_log = os.path.join(settings.BASE_DIR, 'rpa', 'logs_email.csv')
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not os.path.exists(caminho_log):
        with open(caminho_log, 'w') as f:
            f.write("fatura_id,cliente,email,status,erro,data_hora\n")

    with open(caminho_log, 'a') as f:
        f.write(f"{fatura.id},{fatura.cliente.nome},{fatura.cliente.email},{status},{erro},{data_hora}\n")

def enviar_email_individual(fatura, caminho_pdf):
    try:
        assunto = f"Fatura TechSolutions - Vencimento {fatura.data_vencimento.strftime('%d/%m/%Y')}"
        corpo = f"""Olá {fatura.cliente.nome},

Sua fatura da TechSolutions está disponível para pagamento.

Valor: R$ {fatura.valor:.2f}
Vencimento: {fatura.data_vencimento.strftime('%d/%m/%Y')}

Segue em anexo o PDF com os detalhes e QR Code para pagamento.

Atenciosamente,
TechSolutions Ltda
"""
        email = EmailMessage(
            assunto,
            corpo,
            settings.EMAIL_HOST_USER,
            [fatura.cliente.email],
        )

        if os.path.exists(caminho_pdf):
            email.attach_file(caminho_pdf)
        else:
            raise FileNotFoundError(f"PDF não encontrado no caminho: {caminho_pdf}")

        # Se houver configuração SMTP válida, enviar
        if settings.EMAIL_HOST and settings.EMAIL_HOST_USER:
             email.send()
        else:
             print("Simulando envio de e-mail (SMTP não configurado).")

        print(f"E-mail enviado para {fatura.cliente.nome} ({fatura.cliente.email})")

        registrar_log_email(fatura, "sucesso")
        return True

    except Exception as e:
        registrar_log_email(fatura, "falhou", str(e))
        raise e
