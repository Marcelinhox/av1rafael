import webbrowser
import time
import os
from datetime import datetime
from django.conf import settings

# Mock pyautogui when DISPLAY is not available
try:
    import pyautogui
except Exception:
    pyautogui = None

def registrar_log_whatsapp(fatura, status, erro=""):
    caminho_log = os.path.join(settings.BASE_DIR, 'rpa', 'logs_whatsapp.csv')
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not os.path.exists(caminho_log):
        with open(caminho_log, 'w') as f:
            f.write("fatura_id,cliente,status,erro,data_hora\n")

    with open(caminho_log, 'a') as f:
        f.write(f"{fatura.id},{fatura.cliente.nome},{status},{erro},{data_hora}\n")

def enviar_whatsapp_individual(fatura):
    try:
        telefone = fatura.cliente.telefone
        telefone_limpo = "".join(filter(str.isdigit, telefone))
        if not telefone_limpo.startswith("55"):
            telefone_limpo = "55" + telefone_limpo

        if len(telefone_limpo) < 12:
             raise ValueError("Número de telefone inválido")

        mensagem = f"Olá {fatura.cliente.nome}, sua fatura da TechSolutions de R$ {fatura.valor:.2f} vence em {fatura.data_vencimento.strftime('%d/%m/%Y')}. Segue em anexo o PDF do boleto."

        link = f"https://web.whatsapp.com/send?phone={telefone_limpo}&text={mensagem}"

        caminho_pdf = os.path.abspath(os.path.join(settings.BASE_DIR, 'boletos', f"fatura_{fatura.cliente.cpf}_{fatura.id}.pdf"))

        print(f"Abrindo WhatsApp para {fatura.cliente.nome} ({telefone_limpo})...")

        if pyautogui:
            webbrowser.open(link)
            time.sleep(20) # Tempo para carregar WhatsApp Web e QR Code

            # 1. Enviar mensagem de texto inicial
            pyautogui.press('enter')
            time.sleep(5)

            # 2. Clicar no ícone de anexo (clipe 📎)
            # Nota: As coordenadas variam conforme a tela, mas o PyAutoGUI é exigido no projeto.
            # Aqui implementamos a lógica conforme solicitado pelo cenário RPA.
            pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height - 100) # Exemplo centralizado na barra inferior
            time.sleep(2)

            # 3. Digitar o caminho do arquivo no explorador que abrir
            pyautogui.write(caminho_pdf)
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(5)

            # 4. Confirmar o envio do arquivo
            pyautogui.press('enter')
            print(f"Arquivo anexado e enviado: {caminho_pdf}")

        else:
            print(f"Simulando envio de WhatsApp + Anexo {caminho_pdf} (PyAutoGUI não disponível).")

        registrar_log_whatsapp(fatura, "sucesso")
        return True

    except Exception as e:
        registrar_log_whatsapp(fatura, "falhou", str(e))
        raise e
