# 🔴 DANGER LINE v2 — Resumo do Projeto

## Visão Geral

O **Danger Line** é um sistema administrativo e assistente inteligente que utiliza uma **IA base gratuita** (Groq / Gemini Flash / LLM local) para realizar análises, buscas e resumos de código-fonte, preparando contexto otimizado para ser consumido por uma **IA de alta performance** (Claude, GPT-4, Gemini Pro — paga).

O objetivo central é **economizar tokens** da IA paga ao delegar tarefas simples para a IA gratuita e só escalar para a IA potente quando necessário, com um sistema de classificação por **estrelas de dificuldade (1-3★)**.

---

## Problema que Resolve

Desenvolvedores que utilizam IAs pagas para programação gastam muitos tokens em:
- Análise inicial de código que poderia ser feita por uma IA mais simples
- Contexto bruto e não otimizado enviado para a IA potente
- Tarefas repetitivas de mapeamento e documentação
- Falta de controle sobre o consumo de tokens

## Solução Proposta

Um **intermediário inteligente** que:
1. **Analisa** o projeto com IA gratuita
2. **Classifica** a complexidade do problema (1-3★)
3. **Resume e otimiza** o contexto para IA
4. **Delega** apenas o necessário para a IA paga
5. **Monitora** economia de tokens em um painel de controle

---

## Arquitetura em Alto Nível

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Usuário    │───▶│  Danger Line │───▶│  IA Potente  │
│  (Terminal)  │    │  (IA Base)   │    │ (Claude/GPT) │
└──────────────┘    └──────────────┘    └──────────────┘
                           │
                    ┌──────┴──────┐
                    │  Storage    │
                    │ (Obsidian/  │
                    │  Markdown)  │
                    └─────────────┘
```

## Modalidades de Uso

| Modalidade | Descrição |
|------------|-----------|
| **MCP Server** | Integração direta com Antigravity/Gemini CLI via Model Context Protocol |
| **CLI Standalone** | Interface de terminal independente para uso direto |

## Status Atual

- **Versão anterior**: Protótipo funcional com Ollama + CLI + Obsidian
- **Versão nova**: Em fase de planejamento e documentação (este documento)

---

## Tecnologias Planejadas

| Componente | Tecnologia |
|-----------|------------|
| Linguagem | Python 3.11+ |
| IA Base | Groq API (free) / Gemini Flash API / Ollama local |
| IA Potente | Antigravity (Gemini Pro/Claude) via MCP |
| Armazenamento | Markdown files / Obsidian vault |
| Interface | CLI (Rich) + MCP Server (FastMCP) |
| Containerização | Docker (opcional) |
| Gerenciamento | uv (package manager) |

---

> **Próximo passo**: Consultar `DOCUMENTO_PROJETO.MD` para detalhes técnicos completos e `FICHA_TECNICA.MD` para especificações.
