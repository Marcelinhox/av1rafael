from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import qrcode
import os

def gerar_fatura(cliente, cpf, telefone, valor, data_vencimento, status, data_emissao, id_fatura):
    
    pasta = "boletos"
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"{pasta}/fatura_{cpf}_{id_fatura}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=A4)

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "FATURA")

    # Dados
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Cliente: {cliente}")
    c.drawString(50, 730, f"CPF: {cpf}")
    c.drawString(50, 710, f"Telefone: {telefone}")
    c.drawString(50, 690, f"Valor: R$ {valor}")
    c.drawString(50, 670, f"Vencimento: {data_vencimento}")
    c.drawString(50, 650, f"Status: {status}")
    c.drawString(50, 630, f"Emissão: {data_emissao}")

    # 🔥 QR CODE (PIX fake)
    dados_qr = f"Pagamento para {cliente} - R${valor}"

    qr = qrcode.make(dados_qr)
    qr_path = f"{pasta}/qr_{cpf}_{id_fatura}.png"
    qr.save(qr_path)

    c.drawImage(qr_path, 400, 600, width=120, height=120)

    c.save()

    print(f"PDF gerado: {nome_arquivo}")