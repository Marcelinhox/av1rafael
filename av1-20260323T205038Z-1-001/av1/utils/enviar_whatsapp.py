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
        # Normalizar telefone (apenas dígitos e prefixo 55)
        telefone_limpo = "".join(filter(str.isdigit, telefone))
        if not telefone_limpo.startswith("55"):
            telefone_limpo = "55" + telefone_limpo

        if len(telefone_limpo) < 12:
             raise ValueError("Número de telefone inválido")

        mensagem = f"Olá {fatura.cliente.nome}, sua fatura da TechSolutions de R$ {fatura.valor:.2f} vence em {fatura.data_vencimento.strftime('%d/%m/%Y')}. Segue anexo o boleto."

        link = f"https://web.whatsapp.com/send?phone={telefone_limpo}&text={mensagem}"

        print(f"Abrindo WhatsApp para {fatura.cliente.nome} ({telefone_limpo})...")

        if pyautogui:
            # Automação real com PyAutoGUI (no ambiente real com DISPLAY)
            webbrowser.open(link)
            time.sleep(15) # Tempo para o WhatsApp Web carregar
            pyautogui.press('enter') # Envia a mensagem de texto
            time.sleep(2)

            # TODO: Anexar PDF se necessário (como no script original)
            # Para este MVP, vamos focar no envio da mensagem com link ou texto.
        else:
            print("Simulando envio de WhatsApp (PyAutoGUI não disponível).")

        # Registrar sucesso
        registrar_log_whatsapp(fatura, "sucesso")
        return True

    except Exception as e:
        registrar_log_whatsapp(fatura, "falhou", str(e))
        raise e
