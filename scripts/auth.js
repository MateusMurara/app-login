// Inicializa o armazenamento de usuários se não existir
if (!localStorage.usuarios) {
  localStorage.usuarios = JSON.stringify([{ user: 'admin', pass: '123' }]);
}

// Função para mostrar mensagens
function showMessage(elementId, message, isError = true) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = message;
    element.className = isError ? 'alert alert-danger' : 'alert alert-success';
    element.style.display = 'block';
    
    // Rolar até a mensagem
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// Função de login
function login() {
  const userInput = document.getElementById('loginUser');
  const passInput = document.getElementById('loginPass');
  const msgElement = document.getElementById('msgLogin');
  
  const u = userInput.value.trim();
  const p = passInput.value;
  
  // Validação básica
  if (!u || !p) {
    showMessage('msgLogin', 'Por favor, preencha todos os campos.');
    return;
  }
  
  // Simula um atraso de rede
  const loginBtn = document.querySelector('button[onclick="login()"]');
  const originalBtnText = loginBtn.innerHTML;
  loginBtn.disabled = true;
  loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Entrando...';
  
  // Simula um atraso de rede
  setTimeout(() => {
    try {
      const usuarios = JSON.parse(localStorage.usuarios || '[]');
      const usuario = usuarios.find(us => us.user === u && us.pass === p);
      
      if (usuario) {
        localStorage.logado = u;
        showMessage('msgLogin', 'Login realizado com sucesso! Redirecionando...', false);
        
        // Redireciona após um breve atraso
        setTimeout(() => {
          window.location.href = 'menu.html';
        }, 1000);
      } else {
        showMessage('msgLogin', 'Usuário ou senha inválidos.');
        passInput.focus();
      }
    } catch (error) {
      console.error('Erro durante o login:', error);
      showMessage('msgLogin', 'Ocorreu um erro durante o login. Tente novamente.');
    } finally {
      loginBtn.disabled = false;
      loginBtn.innerHTML = originalBtnText;
    }
  }, 800);
}

// Função de registro
function registrar() {
  const userInput = document.getElementById('regUser');
  const passInput = document.getElementById('regPass');
  const msgElement = document.getElementById('msgRegistro');
  
  const u = userInput.value.trim();
  const p = passInput.value;
  
  // Validação
  if (!u || !p) {
    showMessage('msgRegistro', 'Por favor, preencha todos os campos.');
    return;
  }
  
  if (p.length < 4) {
    showMessage('msgRegistro', 'A senha deve ter pelo menos 4 caracteres.');
    passInput.focus();
    return;
  }
  
  const registerBtn = document.querySelector('button[onclick="registrar()"]');
  const originalBtnText = registerBtn.innerHTML;
  registerBtn.disabled = true;
  registerBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registrando...';
  
  // Simula um atraso de rede
  setTimeout(() => {
    try {
      const usuarios = JSON.parse(localStorage.usuarios || '[]');
      
      if (usuarios.find(us => us.user === u)) {
        showMessage('msgRegistro', 'Este nome de usuário já está em uso.');
        userInput.focus();
      } else {
        usuarios.push({ user: u, pass: p });
        localStorage.usuarios = JSON.stringify(usuarios);
        showMessage('msgRegistro', 'Cadastro realizado com sucesso! Redirecionando para o login...', false);
        
        // Redireciona para a página de login após um breve atraso
        setTimeout(() => {
          window.location.href = 'index.html';
        }, 1500);
      }
    } catch (error) {
      console.error('Erro durante o registro:', error);
      showMessage('msgRegistro', 'Ocorreu um erro durante o registro. Tente novamente.');
    } finally {
      registerBtn.disabled = false;
      registerBtn.innerHTML = originalBtnText;
    }
  }, 800);
}

// Função de logout
function logout() {
  // Adiciona um efeito de transição
  document.body.style.opacity = '0.7';
  
  // Simula um atraso para a transição
  setTimeout(() => {
    localStorage.removeItem('logado');
    window.location.href = 'index.html';
  }, 300);
}

// Verifica se o usuário está logado ao carregar páginas protegidas
document.addEventListener('DOMContentLoaded', function() {
  const protectedPages = ['menu.html', 'cadastro.html', 'consulta.html'];
  const currentPage = window.location.pathname.split('/').pop();
  
  if (protectedPages.includes(currentPage) && !localStorage.logado) {
    window.location.href = 'index.html';
  }
  
  // Exibe o nome do usuário logado no menu
  const userDisplay = document.getElementById('userDisplay');
  if (userDisplay && localStorage.logado) {
    userDisplay.textContent = localStorage.logado;
  }
});