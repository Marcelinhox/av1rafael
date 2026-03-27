from django.shortcuts import render
from django.contrib import messages
from .models import Cliente
from utils.gerar_em_lote import executar

def cadastro(request):

    if request.method == 'POST':
        acao = request.POST.get('acao')

        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')

        # -------------------------
        # CADASTRAR CLIENTE
        # -------------------------
        if acao == 'cadastrar':

            if not cpf or not nome or not telefone:
                messages.error(request, "Preencha todos os campos!")
            
            elif Cliente.objects.filter(cpf=cpf).exists():
                messages.error(request, "Cliente já existe!")
            
            else:
                Cliente.objects.create(
                    cpf=cpf,
                    nome=nome,
                    telefone=telefone
                )
                messages.success(request, "Cliente cadastrado com sucesso!")

        # -------------------------
        # GERAR FATURAS
        # -------------------------
        elif acao == 'gerar_pdf':

            if not cpf:
                messages.error(request, "Informe o CPF do cliente!")
            
            else:
                try:
                    cliente = Cliente.objects.get(cpf=cpf)

                    total = executar(cliente)

                    if total > 0:
                        messages.success(request, f"{total} fatura(s) gerada(s) com sucesso!")
                    else:
                        messages.error(request, "Nenhuma fatura encontrada para este cliente.")

                except Cliente.DoesNotExist:
                    messages.error(request, "Cliente não encontrado. Cadastre primeiro.")

    return render(request, 'cadastro.html')