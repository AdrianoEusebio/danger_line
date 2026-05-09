# 📋 FICHA TÉCNICA — DANGER LINE

---

## Identificação do Projeto

| Campo | Valor |
|-------|-------|
| **Nome** | Danger Line |
| **Tipo** | Knowledge Base + MCP Server + CLI |
| **Versão** | 3.0.0 (Refatoração Estratégica) |
| **Linguagem Principal** | Python 3.11+ |
| **Licença** | Privada |
| **Autor** | Adrian |
| **Vault Obsidian** | `C:/Users/adria/OneDrive/Documentos/Danger_line/Danger Line` |

---

## Arquitetura Modular

O sistema é construído sobre dois módulos fundamentais e independentes:

### 1. Módulo MCP (Model Context Protocol)
- **Função**: Interface de comunicação com IAs (Antigravity).
- **Componentes**: FastMCP, handlers de ferramentas, definição de recursos.
- **Responsabilidades**: Expor o KB para a IA, permitir que a IA crie notas, busque contexto e analise projetos.

### 2. Módulo Obsidian (Knowledge Engine)
- **Função**: Gerenciamento do vault e estrutura KB.
- **Componentes**: Leitor/Escritor de Markdown, Linker de notas, Template engine.
- **Responsabilidades**: Manter a integridade do wiki, organizar Project Cards, gerenciar [[wikilinks]] e metadados (frontmatter).

---

## Requisitos de Software

| Dependência | Versão | Obrigatório |
|-------------|--------|-------------|
| Python | 3.11+ | ✅ Sim |
| uv | latest | ✅ Sim |
| Obsidian | 1.5+ | ✅ Sim (Cérebro do sistema) |
| Antigravity IDE | latest | ✅ Sim (Principal cliente MCP) |
| Local REST API | Plugin | 🟡 Recomendado (Para automações via API) |

---

## Stack Tecnológica

### Core & Módulos
| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Runtime | Python 3.11+ | Flexibilidade e ecossistema de IA. |
| MCP Framework | `FastMCP` | Padrão da Anthropic/Google para integração de ferramentas. |
| Obsidian Engine | Custom Python Module | Controle total sobre a estrutura do vault. |
| Package Manager | `uv` | Velocidade e determinismo. |

### IA Providers (Chain of Fallback)
| Provider | Uso |
|----------|-----|
| Gemini Flash 2.0 | Análise de código, extração de padrões, classificação. |
| Groq (Llama 3.3) | Resumos rápidos, fallback de alta performance. |
| Ollama (Local) | Processamento offline e tarefas de baixa complexidade. |

---

## Requisitos Funcionais (Prioritários)

| ID | Requisito | Módulo |
|----|-----------|--------|
| RF-01 | Criar/Atualizar Project Cards no Obsidian automaticamente. | Obsidian |
| RF-02 | Extrair padrões de código e documentar como notas vinculadas. | Obsidian |
| RF-03 | Disponibilizar busca semântica e por wikilinks para a IA. | MCP |
| RF-04 | Permitir que a IA escreva novas descobertas diretamente no KB. | MCP |
| RF-05 | Gerenciar regras de workspace para Antigravity via MCP resources. | MCP |
| RF-06 | Integrar com sistemas externos (ex: Voz) via API modular. | Core |

---

## Estrutura de Diretórios (Refatorada)

```
Danger_line/
├── src/
│   ├── main.py                 # Entry point (CLI / MCP starter)
│   ├── modules/
│   │   ├── mcp/                # Módulo de interface MCP
│   │   │   ├── server.py       # Definição do servidor FastMCP
│   │   │   ├── tools.py        # Ferramentas expostas (search, write, analyze)
│   │   │   └── resources.py    # Recursos (configurações, prompts)
│   │   └── obsidian/           # Módulo de controle do Obsidian
│   │       ├── vault.py        # Gestão de arquivos e pastas
│   │       ├── templates.py    # Templates de Project Cards/Patterns
│   │       └── kb_logic.py     # Lógica de interligação KB
│   ├── core/                   # Lógica compartilhada e orquestração
│   ├── providers/              # Adapters para IAs (Gemini, Groq, Ollama)
│   └── shared/                 # Utilitários, métricas e modelos de dados
├── documents/                  # Documentação atualizada
├── pyproject.toml              # Configuração uv
└── .env                        # Chaves de API e caminhos
```

---

## Métricas de Sucesso
1. **Zero Footprint**: Nenhum arquivo residual em pastas de projetos externos.
2. **KB Hit Rate**: > 50% das dúvidas da IA resolvidas via consulta ao Obsidian.
3. **Escalabilidade**: Adição de novos módulos (ex: Voice) sem alterar o core.
