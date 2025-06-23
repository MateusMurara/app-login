# Registro de usuário existente
# Registro de novo usuário válido
# Login inválido
# Login válido
# Login com novo usuário registrado
# Cadastro inválido (campos vazios)
# Cadastro válido
# Edição de cadastro
# Exclusão de cadastro
# Cancelar cadastro
# Logout

# WebDriverWait:
# Esperar elementos visíveis.

# Esperar URLs atualizadas

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_PATH = "file:///C:/Users/ester/Downloads/app"  

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def esperar_elemento(driver, by, valor, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, valor))
    )

def pausar(segundos=1):
    time.sleep(segundos)

def test_fluxo_completo(driver):
    # --- TENTAR LOGIN INVÁLIDO ---
    driver.get(f"{BASE_PATH}/index.html")
    driver.find_element(By.ID, "loginUser").send_keys("usuarioErrado")
    driver.find_element(By.ID, "loginPass").send_keys("senhaErrada")
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()
    pausar()
    msg_erro_login = esperar_elemento(driver, By.ID, "msgLogin").text
    assert "inválidos" in msg_erro_login.lower()
    pausar()

    # --- LOGIN VÁLIDO ---
    driver.find_element(By.ID, "loginUser").clear()
    driver.find_element(By.ID, "loginPass").clear()
    driver.find_element(By.ID, "loginUser").send_keys("admin")
    driver.find_element(By.ID, "loginPass").send_keys("123")
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()
    WebDriverWait(driver, 5).until(EC.url_contains("menu.html"))
    pausar()
    assert "Menu Principal" in driver.page_source
    pausar()

    # --- TENTAR REGISTRO INVÁLIDO ---
    driver.get(f"{BASE_PATH}/register.html")
    pausar()
    driver.find_element(By.ID, "regUser").send_keys("admin")
    driver.find_element(By.ID, "regPass").send_keys("qualquer")
    driver.find_element(By.XPATH, "//button[text()='Registrar']").click()
    pausar()
    msg_erro_registro = esperar_elemento(driver, By.ID, "msgRegistro").text
    assert "já existe" in msg_erro_registro.lower()
    pausar()

    # --- REGISTRO VÁLIDO ---
    driver.find_element(By.ID, "regUser").clear()
    driver.find_element(By.ID, "regPass").clear()
    driver.find_element(By.ID, "regUser").send_keys("novoUser")
    driver.find_element(By.ID, "regPass").send_keys("senha123")
    driver.find_element(By.XPATH, "//button[text()='Registrar']").click()
    pausar()
    msg_sucesso_registro = esperar_elemento(driver, By.ID, "msgRegistro").text
    assert "sucesso" in msg_sucesso_registro.lower()
    pausar()

    # --- LOGIN COM NOVO USUÁRIO ---
    driver.find_element(By.LINK_TEXT, "Voltar").click()
    WebDriverWait(driver, 5).until(EC.url_contains("index.html"))
    pausar()
    driver.find_element(By.ID, "loginUser").clear()
    driver.find_element(By.ID, "loginPass").clear()
    driver.find_element(By.ID, "loginUser").send_keys("novoUser")
    driver.find_element(By.ID, "loginPass").send_keys("senha123")
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()
    WebDriverWait(driver, 5).until(EC.url_contains("menu.html"))
    pausar()
    assert "Menu Principal" in driver.page_source
    pausar()

    # --- CADASTRO INVÁLIDO (campos vazios) ---
    driver.get(f"{BASE_PATH}/cadastro.html")
    pausar()
    driver.find_element(By.XPATH, "//button[text()='Salvar']").click()
    pausar()
    WebDriverWait(driver, 5).until(EC.url_contains("consulta.html"))
    assert "consulta.html" in driver.current_url
    pausar()

    # --- CADASTRO VÁLIDO ---
    driver.get(f"{BASE_PATH}/cadastro.html")
    pausar()
    driver.find_element(By.ID, "nome").send_keys("Carlos Teste")
    driver.find_element(By.ID, "email").send_keys("carlos@email.com")
    driver.find_element(By.XPATH, "//button[text()='Salvar']").click()
    pausar()
    WebDriverWait(driver, 5).until(EC.url_contains("consulta.html"))
    assert "Carlos Teste" in driver.page_source
    pausar()

    # --- EDITAR CADASTRO ---
    driver.find_element(By.XPATH, "//button[text()='Editar']").click()
    WebDriverWait(driver, 5).until(EC.url_contains("cadastro.html"))
    pausar()
    driver.find_element(By.ID, "nome").clear()
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "nome").send_keys("Carlos Editado")
    driver.find_element(By.ID, "email").send_keys("editado@email.com")
    driver.find_element(By.XPATH, "//button[text()='Salvar']").click()
    pausar()
    WebDriverWait(driver, 5).until(EC.url_contains("consulta.html"))
    assert "Carlos Editado" in driver.page_source
    pausar()

    # --- EXCLUIR CADASTRO ---
    driver.find_element(By.XPATH, "//button[text()='Excluir']").click()
    pausar()
    WebDriverWait(driver, 5).until(EC.url_contains("consulta.html"))
    assert "Carlos Editado" not in driver.page_source
    pausar()

    # --- CADASTRO CANCELADO ---
    driver.get(f"{BASE_PATH}/cadastro.html")
    pausar()
    driver.find_element(By.ID, "nome").send_keys("Teste Cancelar")
    driver.find_element(By.ID, "email").send_keys("cancelar@email.com")
    pausar()
    driver.find_element(By.LINK_TEXT, "Cancelar").click()
    WebDriverWait(driver, 5).until(EC.url_contains("menu.html"))
    assert "Menu Principal" in driver.page_source
    pausar()

    # --- LOGOUT ---
    driver.get(f"{BASE_PATH}/menu.html")
    pausar()
    driver.find_element(By.XPATH, "//button[text()='Logout']").click()
    pausar()
    WebDriverWait(driver, 5).until(EC.url_contains("index.html"))
    assert "Entrar" in driver.page_source

    print("\n Teste de fluxo completo finalizado!")
