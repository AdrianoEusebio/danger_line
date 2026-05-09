# 🔄 IDEIA 4 — Módulo Context Switcher (Múltiplos Cérebros)

## 1. O Problema da Poluição de Contexto
Um desenvolvedor full-stack lida com mundos diferentes (React, NestJS, Docker). Injetar todo o conhecimento de uma vez na IA causa alucinações e desperdício de tokens.

## 2. A Solução: Context Switching
O sistema permite alternar entre bases de conhecimento especializadas, mantendo uma biblioteca central compartilhada.

### A. Categorias de Especialização
- **🧠 Core:** Lógica universal, algoritmos, padrões de código limpo. (Sempre ativo).
- **🔙 Backend:** DBs, APIs, Segurança, Performance Server-side.
- **🎨 Frontend:** UI/UX, State Management, Frameworks CSS/JS.
- **☁️ Infra:** Docker, CI/CD, Scripts de automação.

### B. Como o Switch Funciona
1.  **Detecção Automática:** O Danger Line analisa os arquivos abertos (ex: `.ts`, `package.json`, `.py`) e sugere o contexto ideal.
2.  **Comando Manual:** O desenvolvedor pode trocar o contexto via CLI ou MCP: `set_context("frontend")`.
3.  **Filtragem de Busca:** As ferramentas de busca do MCP priorizam as pastas do contexto ativo no Obsidian.

## 3. Implementação Técnica
- O sistema utiliza **Tags** e **Pastas Raízes** no Obsidian para segmentar o conhecimento.
- No `config.toml`, definimos quais pastas pertencem a quais contextos.
- O prompt enviado para a IA Potente inclui uma pequena "Instrução de Especialista" baseada no cérebro ativo.

## 4. Vantagens
- **Precisão Cirúrgica:** A IA responde com padrões de React quando você está no Frontend, e padrões SQL quando está no Backend.
- **Tokens Otimizados:** O contexto enviado é filtrado para ser o mais relevante possível.
- **Organização:** Seu vault permanece limpo e bem estruturado.

---
> **Status**: Novo módulo estratégico para garantir a alta performance da IA em diferentes stacks.
