// Verifica se o usuário está logado
if (!localStorage.logado) {
  window.location.href = 'index.html';
  throw new Error('Usuário não autenticado');
}

// Inicializa o armazenamento de pessoas se não existir
if (!localStorage.pessoas) {
  localStorage.pessoas = JSON.stringify([]);
}

// Elementos da interface
const nomeInput = document.getElementById('nome');
const emailInput = document.getElementById('email');
const msgCadastro = document.getElementById('msgCadastro');
const tabela = document.getElementById('tabela');

// Variáveis de estado
let pessoas = JSON.parse(localStorage.pessoas);
let editIndex = null;

/**
 * Função para exibir mensagens de feedback
 */
function showMessage(elementId, message, isError = true) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = message;
    element.className = isError ? 'alert alert-danger' : 'alert alert-success';
    element.style.display = 'block';
    
    // Rolar até a mensagem
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Esconder a mensagem após 5 segundos
    setTimeout(() => {
      element.style.display = 'none';
    }, 5000);
  }
}

/**
 * Salva uma nova pessoa ou atualiza uma existente
 */
function salvarPessoa() {
  const nome = nomeInput ? nomeInput.value.trim() : '';
  const email = emailInput ? emailInput.value.trim() : '';
  
  // Validação dos campos
  if (!nome || !email) {
    showMessage('msgCadastro', 'Por favor, preencha todos os campos.');
    return;
  }
  
  // Validação de e-mail simples
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showMessage('msgCadastro', 'Por favor, insira um e-mail válido.');
    return;
  }
  
  // Verifica se já existe uma pessoa com o mesmo e-mail (exceto na edição)
  const emailExists = pessoas.some((pessoa, index) => {
    return pessoa.email.toLowerCase() === email.toLowerCase() && index !== editIndex;
  });
  
  if (emailExists) {
    showMessage('msgCadastro', 'Já existe um cadastro com este e-mail.');
    return;
  }
  
  // Atualiza ou adiciona a pessoa
  if (editIndex !== null) {
    pessoas[editIndex] = { nome, email };
    editIndex = null;
    showMessage('msgCadastro', 'Cadastro atualizado com sucesso!', false);
  } else {
    pessoas.push({ nome, email });
    showMessage('msgCadastro', 'Cadastro realizado com sucesso!', false);
  }
  
  // Salva no localStorage
  localStorage.pessoas = JSON.stringify(pessoas);
  
  // Redireciona para a página de consulta após um breve atraso
  setTimeout(() => {
    window.location.href = 'consulta.html';
  }, 1000);
}

/**
 * Atualiza a tabela de pessoas
 */
function atualizarTabela() {
  if (!tabela) return;
  
  // Ordena as pessoas por nome
  const pessoasOrdenadas = [...pessoas].sort((a, b) => 
    a.nome.localeCompare(b.nome, 'pt-BR', {sensitivity: 'base'})
  );
  
  if (pessoasOrdenadas.length === 0) {
    tabela.innerHTML = `
      <tr>
        <td colspan="3" class="text-center">Nenhum registro encontrado</td>
      </tr>`;
    document.getElementById('tableInfo').textContent = 'Nenhum registro encontrado';
    return;
  }
  
  tabela.innerHTML = pessoasOrdenadas.map((pessoa, index) => {
    // Encontra o índice original para edição/exclusão
    const originalIndex = pessoas.findIndex(p => 
      p.nome === pessoa.nome && p.email === pessoa.email
    );
    
    return `
      <tr>
        <td>${pessoa.nome}</td>
        <td>${pessoa.email}</td>
        <td class="text-center">
          <button class="btn-action btn-edit" onclick="editar(${originalIndex})" 
                  title="Editar">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn-action btn-delete" onclick="confirmarExclusao(${originalIndex})" 
                  title="Excluir">
            <i class="fas fa-trash"></i>
          </button>
        </td>
      </tr>`;
  }).join('');
  
  // Atualiza o contador de registros
  document.getElementById('tableInfo').textContent = 
    `${pessoasOrdenadas.length} registro(s) encontrado(s)`;
}

/**
 * Prepara o formulário para edição
 */
function editar(index) {
  if (index >= 0 && index < pessoas.length) {
    localStorage.setItem('editIndex', index);
    window.location.href = 'cadastro.html';
  }
}

/**
 * Remove uma pessoa da lista
 */
function excluir(index) {
  if (index >= 0 && index < pessoas.length) {
    pessoas.splice(index, 1);
    localStorage.pessoas = JSON.stringify(pessoas);
    
    // Atualiza a tabela na página de consulta
    if (window.location.pathname.endsWith('consulta.html')) {
      atualizarTabela();
    } else {
      window.location.href = 'consulta.html';
    }
  }
}

// Inicialização da página
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPage);
} else {
  initPage();
}

function initPage() {
  // Preenche o formulário se estiver em modo de edição
  if (localStorage.editIndex !== undefined && nomeInput && emailInput) {
    const index = parseInt(localStorage.editIndex);
    if (!isNaN(index) && index >= 0 && index < pessoas.length) {
      nomeInput.value = pessoas[index].nome || '';
      emailInput.value = pessoas[index].email || '';
      editIndex = index;
    }
    // Remove o índice de edição após carregar os dados
    localStorage.removeItem('editIndex');
  }
  
  // Atualiza a tabela se estiver na página de consulta
  if (window.location.pathname.endsWith('consulta.html')) {
    atualizarTabela();
  }
  
  // Adiciona evento de tecla Enter nos formulários
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) submitBtn.click();
      }
    });
  });
}

// Torna as funções disponíveis globalmente
window.salvarPessoa = salvarPessoa;
window.atualizarTabela = atualizarTabela;
window.editar = editar;
window.excluir = excluir;