import pandas as pd
import webbrowser
import time
import pyautogui
import os
from django.conf import settings
from core.models import Cliente
from datetime import datetime

def registrar_erro(cpf, nome, telefone, erro):
    from django.conf import settings
    import os

    caminho_log = os.path.join(settings.BASE_DIR, 'rpa', 'erros.csv')

    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    linha = f"{cpf},{nome},{telefone},{erro},{data_hora}\n"

    # cria cabeçalho se arquivo não existir
    if not os.path.exists(caminho_log):
        with open(caminho_log, 'w') as f:
            f.write("cpf,nome,telefone,erro,data_hora\n")

    with open(caminho_log, 'a') as f:
        f.write(linha)

def enviar_whatsapp():

    caminho_arquivo = os.path.join(settings.BASE_DIR, 'rpa', 'dados', 'faturas.xlsx')

    df = pd.read_excel(caminho_arquivo)

    # normalizar cpf
    df['cpf'] = df['cpf'].astype(str)

    print("Iniciando envio WhatsApp...")

    for index, row in df.iterrows():

        cpf = str(row['cpf'])

        try:
            cliente = Cliente.objects.get(cpf=cpf)
            telefone = cliente.telefone
        except Cliente.DoesNotExist:
            print(f"Cliente com CPF {cpf} não encontrado no banco.")

            registrar_erro(cpf, "N/A", "N/A", "cliente nao encontrado")

            continue

        # valida telefone
        if not telefone or len(telefone) < 10:
            print(f"Telefone inválido para CPF {cpf}, pulando...")

            registrar_erro(cpf, cliente.nome, telefone, "telefone invalido")

            continue

        telefone = "55" + telefone

        mensagem = f"Olá {cliente.nome}, sua fatura de R$ {row['valor']} vence em {row['data_vencimento']}."

        link = f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem}"

        print(f"\nEnviando para: {cliente.nome} - {telefone}")

        # abrir WhatsApp
        webbrowser.open(link)

        # ⏳ primeira vez precisa mais tempo
        if index == 0:
            print("Escaneie o QR Code do WhatsApp Web...")
            time.sleep(20)
        else:
            time.sleep(10)

        # envia mensagem
        pyautogui.press('enter')

        # -------------------------
        # ENVIO DO PDF
        # -------------------------

        caminho_pdf = os.path.join(
            settings.BASE_DIR,
            'boletos',
            f"fatura_{cliente.cpf}_{row['id']}.pdf"
        )

        if not os.path.exists(caminho_pdf):
            print(f"PDF não encontrado: {caminho_pdf}")

            registrar_erro(cpf, cliente.nome, telefone, "pdf nao encontrado")

            continue

        time.sleep(5)

        # clicar no clip (📎) → AJUSTAR POSIÇÃO NA SUA TELA
        pyautogui.click(x=1000, y=700)

        time.sleep(2)

        # clicar em "Documento"
        pyautogui.click(x=1000, y=600)

        time.sleep(2)

        # digitar caminho do arquivo
        pyautogui.write(caminho_pdf)
        time.sleep(2)

        pyautogui.press('enter')
        time.sleep(5)

        # enviar arquivo
        pyautogui.press('enter')

        print("Mensagem + PDF enviados!")

        time.sleep(5)

        # fechar aba
        pyautogui.hotkey('ctrl', 'w')

        time.sleep(3)

    print("\nEnvio finalizado!")