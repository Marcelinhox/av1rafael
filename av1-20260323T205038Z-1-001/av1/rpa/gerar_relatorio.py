import os
import pandas as pd
import sqlite3
from datetime import datetime

def gerar_relatorio_gerente():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"Erro: Banco de dados {db_path} não encontrado.")
        return

    try:
        # Conectar ao SQLite3 do Django
        conn = sqlite3.connect(db_path)

        # Query para juntar Clientes e Faturas
        query = """
        SELECT
            c.nome,
            c.cpf,
            c.email,
            c.telefone,
            f.id as fatura_id,
            f.valor,
            f.data_vencimento,
            f.status,
            f.data_emissao
        FROM core_fatura f
        JOIN core_cliente c ON f.cliente_id = c.id
        """

        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("Nenhum dado encontrado para o relatório.")
            return

        # Caminho do relatório
        relatorio_path = 'rpa/faturas_relatorio.xlsx'
        os.makedirs(os.path.dirname(relatorio_path), exist_ok=True)

        # Exportar para Excel com formatação básica
        writer = pd.ExcelWriter(relatorio_path, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Relatório de Cobrança')

        # Ajustar largura das colunas
        workbook = writer.book
        worksheet = writer.sheets['Relatório de Cobrança']
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + i)].width = column_len

        writer.close()
        print(f"Relatório gerado com sucesso em: {relatorio_path}")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")

if __name__ == "__main__":
    gerar_relatorio_gerente()
