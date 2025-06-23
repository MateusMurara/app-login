# Sistema de Cadastro

Um sistema web simples para gerenciamento de cadastros de pessoas com autenticação de usuários.

## Funcionalidades

- **Autenticação de Usuários**
  - Login e logout
  - Registro de novos usuários
  - Proteção de rotas autenticadas

- **Cadastro de Pessoas**
  - Adicionar novas pessoas
  - Visualizar lista de cadastros
  - Editar cadastros existentes
  - Excluir cadastros
  - Buscar cadastros
  - Ordenação por nome

- **Interface Amigável**
  - Design responsivo
  - Feedback visual para ações
  - Validação de formulários
  - Ícones intuitivos

## Tecnologias Utilizadas

- HTML5
- CSS3 (com variáveis CSS)
- JavaScript puro (ES6+)
- LocalStorage para armazenamento de dados
- Font Awesome para ícones

## Como Executar

1. Clone o repositório ou faça o download dos arquivos
2. Abra o arquivo `index.html` em um navegador web moderno
   - Ou utilize um servidor local (recomendado):
     ```bash
     # Com Python 3
     python -m http.server 8000
     
     # Ou com Python 2
     python -m SimpleHTTPServer 8000
     ```
3. Acesse `http://localhost:8000` no navegador

## Credenciais Padrão

- **Usuário:** admin
- **Senha:** 123

## Estrutura do Projeto

```
app/
├── css/
│   └── style.css          # Estilos principais
├── scripts/
│   ├── auth.js           # Lógica de autenticação
│   ├── crud.js           # Operações CRUD
│   └── util.js           # Funções utilitárias
├── index.html            # Página de login
├── register.html         # Página de registro
├── menu.html             # Menu principal
├── cadastro.html         # Formulário de cadastro
├── consulta.html         # Lista de cadastros
└── README.md            # Documentação
```

## Melhorias Futuras

- [ ] Adicionar confirmação antes de excluir
- [ ] Implementar paginação na lista de cadastros
- [ ] Adicionar exportação para CSV/Excel
- [ ] Melhorar a validação de formulários
- [ ] Adicionar recuperação de senha
- [ ] Implementar upload de fotos

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
