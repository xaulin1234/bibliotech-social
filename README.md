# 📚 Bibliotech Social — Mini Biblioteca Pessoal & Rede de Leitura

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.2-green?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/Licença-MIT-brightgreen?style=for-the-badge)

O **Bibliotech Social** é uma plataforma web completa desenvolvida para leitores organizarem suas bibliotecas pessoais e compartilharem experiências literárias. O sistema une a gestão de acervo físico e lista de desejos à dinâmica social de feed, permitindo a publicação de resenhas, curtidas e comentários em comunidade.

---

## 📌 Funcionalidades Principais

- **Gerenciamento de Acervo:** Cadastro de livros físicos com registro da data exata de aquisição.
- **Lista de Desejos:** Organização de leituras futuras e controle de status de posse ("Quero Ler", "Lido", "Possuo").
- **Feed Social:** Publicação de resenhas vinculadas aos livros da biblioteca.
- **Engajamento:** Sistema de curtidas e área de comentários em tempo real.
- **Perfis Personalizados:** Biografia, estatísticas de leitura e estante individual pública.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

| Biblioteca / Ferramenta | Versão | Descrição / Finalidade |
| :--- | :--- | :--- |
| **Python** | `3.10.x` | Linguagem base para o desenvolvimento backend. |
| **Flask** | `3.0.2` | Micro-framework web para roteamento e controle da aplicação. |
| **Flask-SQLAlchemy** | `3.1.1` | ORM para mapeamento objeto-relacional de dados. |
| **SQLAlchemy** | `2.0.27` | Engine de manipulação do banco de dados relacional. |
| **Werkzeug** | `3.0.1` | Gerenciamento de segurança de senhas (`hash/check_password`). |
| **Jinja2** | `3.1.3` | Motor de templates para renderização dinâmica das páginas HTML. |
| **SQLite3** | Native | Banco de dados relacional embutido para persistência leve. |

---

## 📁 Estrutura de Pastas do Projeto

```text
bibliotech-social/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Estilização global da interface
│   │   ├── js/
│   │   │   └── main.js           # Scripts de interação dinâmica (likes/feed)
│   │   └── img/
│   │       └── avatars/          # Imagens de perfil padrão
│   ├── templates/
│   │   ├── base.html             # Layout base compartilhado (Jinja2)
│   │   ├── index.html            # Feed principal e publicações
│   │   ├── login.html            # Tela de autenticação de usuários
│   │   ├── registro.html         # Cadastro de novos leitores
│   │   ├── acervo.html           # Gestão da biblioteca pessoal
│   │   └── perfil.html           # Exibição do perfil e estatísticas
│   ├── __init__.py               # Inicialização da aplicação Flask e ORM
│   ├── models.py                 # Entidades do banco de dados (User, Book, Review, etc.)
│   └── routes.py                 # Rotas da aplicação e regras de negócio
├── docs/
│   ├── diagrama_classes.png      # Diagrama UML da estrutura do banco de dados
│   └── diagrama_casos_uso.png    # Diagrama de Casos de Uso do sistema
├── instance/
│   └── database.db               # Arquivo de banco de dados local SQLite
├── .gitignore                    # Arquivos ignorados pelo Git
├── README.md                     # Documentação oficial do repositório
├── requirements.txt              # Lista de dependências do projeto
└── run.py                        # Ponto de entrada para execução da aplicação
