from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

with webdriver.Chrome() as driver:
    driver.get("http://127.0.0.1:8000")

    wait = WebDriverWait(driver, 10)

    df = pd.read_excel('dados/faturas.xlsx')

    for index, row in df.iterrows():
        wait.until(EC.presence_of_element_located((By.NAME, "cpf")))

        # CPF
        driver.find_element(By.NAME, "cpf").clear()
        driver.find_element(By.NAME, "cpf").send_keys(str(row['cpf']))

        # Nome
        driver.find_element(By.NAME, "nome").clear()
        driver.find_element(By.NAME, "nome").send_keys("Cliente " + str(index + 1))

        # Telefone (PEGANDO DO EXCEL)
        telefone = str(row['telefone'])
        telefone = telefone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

        driver.find_element(By.NAME, "telefone").clear()
        driver.find_element(By.NAME, "telefone").send_keys(telefone)

        # Cadastrar
        driver.find_element(By.XPATH, "//button[@value='cadastrar']").click()
        time.sleep(2)

        # Verificação
        page = driver.page_source.lower()

        if "já existe" in page:
            print(f"Cliente {row['cpf']} já existe, pulando...")
            continue

        if "sucesso" in page:
            print(f"Cliente {index + 1} cadastrado com sucesso.")
        else:
            print(f"Erro ao cadastrar cliente {index + 1}")

    # Gerar faturas no final
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@value='gerar_pdf']")))
    driver.find_element(By.XPATH, "//button[@value='gerar_pdf']").click()