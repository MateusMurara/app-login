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

BASE_PATH = "file:///C:/Users/mateu/Documents/Faculdade/app-login"  

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
    
    # Executa a função de login diretamente
    driver.execute_script("login()")
    
    # Aguarda a mensagem de erro
    pausar(2)  # Dá tempo para a animação e validação
    
    # Verifica se a mensagem de erro foi exibida
    msg_erro = esperar_elemento(driver, By.ID, "msgLogin")
    assert "display: none" not in msg_erro.get_attribute("style"), "Mensagem de erro não foi exibida"
    assert "Usuário ou senha inválidos" in msg_erro.text, "Mensagem de erro incorreta"

    # --- LOGIN VÁLIDO ---
    driver.find_element(By.ID, "loginUser").clear()
    driver.find_element(By.ID, "loginPass").clear()
    driver.find_element(By.ID, "loginUser").send_keys("admin")
    driver.find_element(By.ID, "loginPass").send_keys("123")
    
    # Executa a função de login diretamente
    driver.execute_script("login()")
    
    # Aguarda o redirecionamento para o menu
    pausar(2)  # Dá tempo para o redirecionamento
    WebDriverWait(driver, 5).until(EC.url_contains("menu.html"))
    pausar()
    assert "Menu Principal" in driver.page_source
    pausar()

    # --- TENTAR REGISTRO INVÁLIDO ---
    driver.get(f"{BASE_PATH}/register.html")
    pausar()
    driver.find_element(By.ID, "regUser").send_keys("admin")
    driver.find_element(By.ID, "regPass").send_keys("qualquer")
    
    # Executa a função de registro diretamente
    driver.execute_script("registrar()")
    
    # Aguarda a mensagem de erro
    pausar(2)  # Dá tempo para a animação e validação
    
    # Verifica se a mensagem de erro foi exibida
    msg_erro = esperar_elemento(driver, By.ID, "msgRegistro")
    assert "display: none" not in msg_erro.get_attribute("style"), "Mensagem de erro não foi exibida"
    assert "Este nome de usuário já está em uso" in msg_erro.text, "Mensagem de erro incorreta"
    pausar()

    # --- REGISTRO VÁLIDO ---
    driver.find_element(By.ID, "regUser").clear()
    driver.find_element(By.ID, "regPass").clear()
    driver.find_element(By.ID, "regUser").send_keys("novoUser")
    driver.find_element(By.ID, "regPass").send_keys("senha123")
    # Usa o mesmo método de clique via JavaScript que foi usado anteriormente
    driver.execute_script("registrar()")
    pausar()
    msg_sucesso_registro = esperar_elemento(driver, By.ID, "msgRegistro").text
    assert "sucesso" in msg_sucesso_registro.lower()
    pausar()

    # --- LOGIN COM NOVO USUÁRIO ---
    # Usa o link de login que está na página de registro
    driver.find_element(By.LINK_TEXT, "Faça login aqui").click()
    WebDriverWait(driver, 5).until(EC.url_contains("index.html"))
    pausar()
    driver.find_element(By.ID, "loginUser").clear()
    driver.find_element(By.ID, "loginPass").clear()
    driver.find_element(By.ID, "loginUser").send_keys("novoUser")
    driver.find_element(By.ID, "loginPass").send_keys("senha123")
    # Usa o mesmo método de clique via JavaScript que foi usado anteriormente
    driver.execute_script("login()")
    WebDriverWait(driver, 5).until(EC.url_contains("menu.html"))
    pausar()
    assert "Menu Principal" in driver.page_source
    pausar()

    # --- CADASTRO INVÁLIDO (campos vazios) ---
    driver.get(f"{BASE_PATH}/cadastro.html")
    pausar()
    driver.execute_script("salvarPessoa()")
    pausar()
    # Verifica a mensagem de erro
    msg_erro = esperar_elemento(driver, By.ID, "msgCadastro")
    assert "display: none" not in msg_erro.get_attribute("style"), "Mensagem de erro não foi exibida"
    assert "por favor, preencha todos os campos" in msg_erro.text.lower(), "Mensagem de erro incorreta"
    pausar()

    # --- CADASTRO VÁLIDO ---
    driver.get(f"{BASE_PATH}/cadastro.html")
    pausar()
    driver.find_element(By.ID, "nome").send_keys("Carlos Teste")
    driver.find_element(By.ID, "email").send_keys("carlos@email.com")
    driver.execute_script("salvarPessoa()")
    pausar()
    WebDriverWait(driver, 5).until(EC.url_contains("consulta.html"))
    assert "Carlos Teste" in driver.page_source
    pausar()

    # --- EDITAR CADASTRO ---
    # Espera a tabela carregar
    pausar(2)
    # Encontra o botão de editar pelo ícone
    btn_editar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-edit i.fa-edit"))
    )
    # Clica no botão de editar
    driver.execute_script("arguments[0].click();", btn_editar)
    
    # Aguarda o carregamento da página de cadastro
    WebDriverWait(driver, 10).until(EC.url_contains("cadastro.html"))
    pausar()
    
    # Limpa e preenche os campos
    driver.find_element(By.ID, "nome").clear()
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "nome").send_keys("Carlos Editado")
    driver.find_element(By.ID, "email").send_keys("editado@email.com")
    
    # Salva as alterações
    driver.execute_script("salvarPessoa()")
    pausar(2)  # Dá tempo para salvar e redirecionar
    
    # Verifica se voltou para a página de consulta e se o nome editado está visível
    WebDriverWait(driver, 10).until(EC.url_contains("consulta.html"))
    assert "Carlos Editado" in driver.page_source, "O nome editado não foi encontrado na página"
    pausar()

    # --- EXCLUIR CADASTRO ---
    # Encontra o botão de excluir pelo ícone
    btn_excluir = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-delete i.fa-trash"))
    )
    # Clica no botão de excluir
    driver.execute_script("arguments[0].click();", btn_excluir)
    
    # Aguarda o modal de confirmação e confirma a exclusão
    pausar(1)  # Dá tempo para o modal aparecer
    
    # Clica no botão de confirmação do modal
    btn_confirmar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnConfirmar"))
    )
    driver.execute_script("arguments[0].click();", btn_confirmar)
    
    # Aguarda a atualização da página
    pausar(2)  # Dá tempo para a exclusão e atualização da página
    
    # Verifica se o registro foi removido
    assert "Carlos Editado" not in driver.page_source, "O registro não foi removido corretamente"
    pausar()

    # --- CADASTRO CANCELADO ---
    driver.get(f"{BASE_PATH}/cadastro.html")
    pausar()
    driver.find_element(By.ID, "nome").send_keys("Teste Cancelar")
    driver.find_element(By.ID, "email").send_keys("cancelar@email.com")
    pausar()
    
    # Encontra e clica no botão Cancelar
    btn_cancelar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-secondary"))
    )
    driver.execute_script("arguments[0].click();", btn_cancelar)
    
    # Verifica se voltou para o menu
    WebDriverWait(driver, 10).until(EC.url_contains("menu.html"))
    assert "Menu Principal" in driver.page_source, "Não foi redirecionado para o menu após cancelar"
    pausar()

    # --- LOGOUT ---
    driver.get(f"{BASE_PATH}/menu.html")
    pausar()
    
    # Encontra e clica no botão de logout (pode ser "Sair" ou "Sair do Sistema")
    try:
        # Tenta encontrar o botão "Sair" no cabeçalho
        btn_logout = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sair')]"))
        )
    except:
        # Se não encontrar, tenta o botão "Sair do Sistema" no menu principal
        btn_logout = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sair do Sistema')]"))
        )
    
    driver.execute_script("arguments[0].click();", btn_logout)
    pausar(2)  # Dá tempo para o logout e redirecionamento
    
    # Verifica se foi redirecionado para a página de login
    WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
    assert "Entrar" in driver.page_source, "Não foi redirecionado para a página de login após o logout"

    print("\nTeste de fluxo completo finalizado com sucesso!")
