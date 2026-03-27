import pandas as pd
import os
from django.conf import settings
from utils.gerar_pdf import gerar_fatura
from core.models import Fatura

def executar(cliente):

    caminho_arquivo = os.path.join(settings.BASE_DIR, 'rpa', 'dados', 'faturas.xlsx')

    if not os.path.exists(caminho_arquivo):
        print("Arquivo Excel não encontrado!")
        return 0

    print("Lendo arquivo:", caminho_arquivo)

    df = pd.read_excel(caminho_arquivo)

    print("Total de registros:", len(df))

    # normalizar CPF
    df['cpf'] = df['cpf'].astype(str)
    cpf_cliente = str(cliente.cpf)

    print("CPF buscado:", cpf_cliente)

    faturas_cliente = df[df['cpf'] == cpf_cliente]

    print("Faturas encontradas:", len(faturas_cliente))

    total = 0

    for index, row in faturas_cliente.iterrows():

        # 🔥 SALVA NO BANCO
        fatura = Fatura.objects.create(
            cliente=cliente,
            valor=row['valor'],
            data_vencimento=row['data_vencimento'],
            status=row['status'],
            data_emissao_boleto=row['data_emissao_boleto']
        )

        # 🔥 GERA PDF usando ID do banco
        gerar_fatura(
            cliente=cliente.nome,
            cpf=cliente.cpf,
            telefone=cliente.telefone,
            valor=row['valor'],
            data_vencimento=row['data_vencimento'],
            status=row['status'],
            data_emissao=row['data_emissao_boleto'],
            id_fatura=fatura.id  # 👈 IMPORTANTE
        )

        total += 1

    return total