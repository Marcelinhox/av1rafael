from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Fatura
from utils.gerar_pdf import gerar_fatura
from utils.enviar_whatsapp import enviar_whatsapp_individual
from utils.enviar_email import enviar_email_individual
import os
from django.conf import settings
from datetime import datetime

def cadastro(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'cadastrar':
            nome = request.POST.get('nome')
            cpf = request.POST.get('cpf')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            endereco = request.POST.get('endereco')

            if not nome or not cpf or not email or not telefone:
                messages.error(request, "Preencha todos os campos obrigatórios!")
            elif Cliente.objects.filter(cpf=cpf).exists():
                messages.error(request, "Cliente com este CPF já cadastrado!")
            else:
                Cliente.objects.create(
                    nome=nome,
                    cpf=cpf,
                    email=email,
                    telefone=telefone,
                    endereco=endereco
                )
                messages.success(request, f"Cliente {nome} cadastrado com sucesso!")

        elif acao == 'gerar_fatura':
            cliente_id = request.POST.get('cliente_id')
            valor = request.POST.get('valor')
            data_vencimento_str = request.POST.get('data_vencimento')

            if not cliente_id or not valor or not data_vencimento_str:
                messages.error(request, "Preencha todos os campos da fatura!")
            else:
                try:
                    cliente = Cliente.objects.get(id=cliente_id)
                    data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()
                    fatura = Fatura.objects.create(
                        cliente=cliente,
                        valor=float(valor),
                        data_vencimento=data_vencimento
                    )
                    # Gera o PDF logo após criar a fatura
                    gerar_fatura(fatura)
                    messages.success(request, f"Fatura de R$ {valor} gerada para {cliente.nome}!")
                except Exception as e:
                    messages.error(request, f"Erro ao gerar fatura: {e}")

        elif acao == 'gerar_pdf_em_lote':
            faturas = Fatura.objects.all()
            total = 0
            for fatura in faturas:
                try:
                    gerar_fatura(fatura)
                    total += 1
                except Exception as e:
                    print(f"Erro ao gerar PDF da fatura {fatura.id}: {e}")

            if total > 0:
                messages.success(request, f"{total} faturas processadas e PDFs gerados/atualizados.")
            else:
                messages.warning(request, "Nenhuma fatura encontrada para processar em lote.")

    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'cadastro.html', {'clientes': clientes})

def listagem_faturas(request):
    faturas = Fatura.objects.all().order_by('-data_vencimento')
    return render(request, 'listagem_faturas.html', {'faturas': faturas})

def notificar_fatura(request, fatura_id):
    if request.method == 'POST':
        fatura = get_object_or_404(Fatura, id=fatura_id)
        tipo = request.POST.get('tipo')

        caminho_pdf = os.path.join(settings.BASE_DIR, 'boletos', f"fatura_{fatura.cliente.cpf}_{fatura.id}.pdf")

        # Garante que o PDF existe, senão gera
        if not os.path.exists(caminho_pdf):
             gerar_fatura(fatura)

        if tipo == 'whatsapp':
            try:
                enviar_whatsapp_individual(fatura)
                fatura.status = 'enviado'
                fatura.save()
                messages.success(request, f"Notificação via WhatsApp para {fatura.cliente.nome} enviada!")
            except Exception as e:
                fatura.status = 'falhou'
                fatura.save()
                messages.error(request, f"Erro ao notificar via WhatsApp: {e}")

        elif tipo == 'email':
            try:
                enviar_email_individual(fatura, caminho_pdf)
                fatura.status = 'enviado'
                fatura.save()
                messages.success(request, f"E-mail para {fatura.cliente.nome} enviado!")
            except Exception as e:
                fatura.status = 'falhou'
                fatura.save()
                messages.error(request, f"Erro ao enviar e-mail: {e}")

    return redirect('listagem_faturas')
