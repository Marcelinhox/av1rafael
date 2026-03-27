from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
import qrcode
import os
from django.conf import settings

def gerar_fatura(fatura):
    pasta = "boletos"
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"{pasta}/fatura_{fatura.cliente.cpf}_{fatura.id}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    width, height = A4

    # --- Header with company info ---
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1 * cm, height - 2 * cm, "TechSolutions Ltda")

    c.setFont("Helvetica", 10)
    c.drawString(1 * cm, height - 2.5 * cm, "Rua do Financeiro, 123 - Centro")
    c.drawString(1 * cm, height - 3 * cm, "Telefone: (11) 4004-0000 | financeiro@techsolutions.com")

    # --- Horizontal line ---
    c.setStrokeColor(colors.blue)
    c.line(1 * cm, height - 3.5 * cm, width - 1 * cm, height - 3.5 * cm)

    # --- Fatura title and Number ---
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(width - 1 * cm, height - 2 * cm, "FATURA DE COBRANÇA")

    c.setFont("Helvetica", 12)
    c.drawRightString(width - 1 * cm, height - 2.8 * cm, f"Número: {fatura.id:06d}")
    c.drawRightString(width - 1 * cm, height - 3.3 * cm, f"Emissão: {fatura.data_emissao.strftime('%d/%m/%Y')}")

    # --- Client Data Section ---
    c.setFillColor(colors.lightgrey)
    c.rect(1 * cm, height - 7 * cm, width - 2 * cm, 1 * cm, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1.5 * cm, height - 6.6 * cm, "DADOS DO CLIENTE")

    c.setFont("Helvetica", 11)
    c.drawString(1 * cm, height - 7.5 * cm, f"Nome: {fatura.cliente.nome}")
    c.drawString(1 * cm, height - 8.1 * cm, f"CPF: {fatura.cliente.cpf}")
    c.drawString(1 * cm, height - 8.7 * cm, f"Telefone: {fatura.cliente.telefone}")
    c.drawString(1 * cm, height - 9.3 * cm, f"Endereço: {fatura.cliente.endereco or 'Não informado'}")

    # --- Billing Data Section ---
    c.setFillColor(colors.lightgrey)
    c.rect(1 * cm, height - 12 * cm, width - 2 * cm, 1 * cm, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1.5 * cm, height - 11.6 * cm, "DETALHAMENTO DA COBRANÇA")

    c.setFont("Helvetica", 12)
    c.drawString(1 * cm, height - 13 * cm, "Descrição: Serviços de consultoria e suporte técnico")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * cm, height - 14.5 * cm, f"VALOR TOTAL: R$ {fatura.valor:,.2f}")
    c.drawString(1 * cm, height - 15.2 * cm, f"VENCIMENTO: {fatura.data_vencimento.strftime('%d/%m/%Y')}")

    # --- QR Code Section ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(12 * cm, height - 18 * cm, "PAGAMENTO VIA PIX")

    # QR Code com CPF via settings (variável de ambiente)
    pix_key = getattr(settings, 'PIX_KEY_CPF', '12571848909')
    dados_pix = f"PIX-CHAVE-CPF-{pix_key}-FATURA-{fatura.id}-VALOR-{fatura.valor}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(dados_pix)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_path = f"{pasta}/qr_{fatura.id}.png"
    img.save(qr_path)

    c.drawImage(qr_path, 12 * cm, height - 25 * cm, width=6 * cm, height=6 * cm)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(12 * cm, height - 25.5 * cm, f"Escaneie o QR Code acima para pagar (Chave: {pix_key})")

    # --- Footer ---
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 1.5 * cm, "Obrigado pela sua preferência! TechSolutions Ltda")

    c.save()
    if os.path.exists(qr_path):
        os.remove(qr_path)

    print(f"PDF profissional gerado: {nome_arquivo}")
    return nome_arquivo
