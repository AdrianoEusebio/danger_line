# 🔴 DANGER LINE — Resumo do Projeto

## Visão Geral

O **Danger Line** é um **Servidor MCP (Model Context Protocol)** nativo que atua como uma ponte entre a **IDE Antigravity** e o **Obsidian**. Ele transforma o seu Vault do Obsidian em uma base de conhecimento (Knowledge Base) dinâmica e consultável em tempo real pela inteligência artificial.

## A Simplificação (Nova Arquitetura)

Na sua refatoração mais recente, o projeto optou pelo **foco absoluto e simplicidade**:
- **Apenas MCP:** Foram removidas interfaces secundárias (CLI de painel, APIs HTTP). O sistema é puramente uma extensão MCP para a IDE.
- **IA da IDE:** A lógica de classificação de arquivos, stacks de desenvolvimento (Frontend/Backend) e análise via LLMs externos (Groq, Gemini Flash, Ollama) foi **completamente removida**. Toda a inteligência de inferência é delegada à IA assistente que já está na IDE (Antigravity).
- **Foco no Obsidian:** O Danger Line brilha em manter a integridade dos dados, formatar Markdown corretamente (com `[[wikilinks]]` e frontmatter YAML) e gerenciar a organização do conhecimento gerado.

---

## Problema que Resolve

Ao longo do desenvolvimento, a IA da IDE sofre de "amnésia" entre sessões. Se um bug complexo for resolvido, na semana seguinte a IA não lembrará dele a menos que seja lembrada. 

## Solução Proposta

Um servidor local leve e rápido que:
1. Permite à IA (Antigravity) **pesquisar** soluções e padrões passados diretamente do Obsidian do desenvolvedor.
2. Permite à IA **registrar (commitar)** novos aprendizados e manuais técnicos de forma automatizada no formato que o Obsidian espera.

---

## Arquitetura em Alto Nível

```
┌──────────────┐      ┌───────────────┐      ┌──────────────┐
│  Antigravity │◀────▶│  Danger Line  │◀────▶│   Obsidian   │
│ (Assistente) │ MCP  │ (Servidor KB) │ DFS  │ (Vault Local)│
└──────────────┘      └───────────────┘      └──────────────┘
```

A arquitetura foi redesenhada para ser altamente escalável no nível do código. Utiliza **classes default e reutilizáveis** para acesso ao File System, formatação de Markdown e roteamento de MCP. Assim, novas "ferramentas" (tools) podem ser adicionadas com facilidade no futuro sem aumentar a complexidade do código fonte.

---

> **Próximo passo**: Consultar `DOCUMENTO_PROJETO.MD` para detalhes da nova arquitetura modular e `FICHA_TECNICA.MD` para especificações técnicas.
