# 🚀 ROADMAP TDD — DANGER LINE

Este documento serve como a "Definição de Pronto" para o sistema, cobrindo desde as bases fundamentais até a inteligência avançada do Ecossistema Agnóstico.

---

## 🟢 FASE 1: Fundação e Infraestrutura (O Básico) [CONCLUÍDO]
- [x] **Configuração do Workspace**: Inicializar projeto com `uv`, configurar `pyproject.toml` e estrutura `src/`.
- [x] **Gestão de Config**: Módulo para carregar `.env`, validar caminhos do Obsidian e chaves de API.
- [x] **Server FastMCP**: Servidor básico rodando e sendo detectado por clientes MCP (Antigravity/Claude).
- [x] **Módulo de Logging**: Sistema de logs centralizado para depuração do sistema.

## 🟡 FASE 2: Módulo Obsidian (A Engrenagem) [CONCLUÍDO]
- [x] **DFS (Direct File System)**: Implementar leitura e escrita de Markdown com preservação de codificação.
- [x] **LRA (Local REST API)**: Cliente HTTP para comunicação com o plugin do Obsidian (Auth + Endpoints base).
- [x] **Template Engine**: Sistema para injetar dados em notas de Specs, Playbooks e Bugfixes.
- [x] **Vault Manager**: Lógica de organização de pastas e navegação entre `Core`, `Backend`, `Frontend`, etc.

## 🛡️ FASE 3: Módulo Sanitizer (A Segurança) [CONCLUÍDO]
- [x] **Static Shield**: Regex para bloqueio de chaves de API, segredos e arquivos proibidos (`.env`).
- [x] **Dynamic Scrubber**: Integração com IA base para limpeza de dados sensíveis em textos dinâmicos.
- [x] **Anonymizer**: Módulo para transformar referências privadas em conceitos genéricos/técnicos.

## 🔄 FASE 4: Context Switcher (Múltiplos Cérebros) [CONCLUÍDO]
- [x] **State Manager**: Controle do contexto ativo (Ex: `ctx = "backend"`).
- [x] **Context Filter**: Função que filtra as buscas e injeção de contexto baseada na pasta ativa do Obsidian.
- [x] **Auto-Detection**: Lógica para sugerir a troca de cérebro baseada na extensão e conteúdo dos arquivos abertos.

## 🧠 FASE 5: Core & Destilação KB (A Inteligência) [CONCLUÍDO]
- [x] **Distiller Engine**: Prompt system para transformar logs/códigos brutos em notas no formato "IA-Optimized".
- [x] **Knowledge Linker**: Criação automática de `[[wikilinks]]` entre novas descobertas e o conhecimento global.
- [x] **Semantic Search**: Interface de busca que consulta o Obsidian e retorna o contexto mais denso para a IA.

## 🔌 FASE 6: Interface MCP & E2E (O Produto) [CONCLUÍDO]
- [x] **Tool: `query_kb`**: Permite que a IA busque soluções e especificações no Obsidian.
- [x] **Tool: `commit_knowledge`**: Permite que a IA salve novos padrões e resoluções de bugs diretamente no KB.
- [x] **AI Adapter Layer**: Garantir que o sistema funcione trocando o provider (Gemini <-> Groq <-> Ollama).
- [x] **Validation Walkthrough**: Teste real de ponta a ponta: Identificar bug -> Buscar no KB -> Resolver -> Salvar nova Spec.

---

## 📈 Progresso Geral: [ 100% ]
*(Atualizar este documento a cada milestone concluído)*
