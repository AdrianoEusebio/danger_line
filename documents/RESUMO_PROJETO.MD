# 🔴 DANGER LINE v5.0 — Resumo do Projeto (DragonScale MCP Edition)

## Visão Geral

O **Danger Line v5.0** é um **Servidor MCP (Model Context Protocol)** nativo em Python projetado para conectar a **IDE Antigravity** ao seu cérebro digital central: o **Obsidian**. Ele atua como um motor local e ultra-rápido de Knowledge Base (KB), que persiste o contexto de engenharia de software e evita a amnésia das sessões da IDE.

O sistema adota uma filosofia portátil, robusta e extensível, fundindo o melhor do design direto via sistema de arquivos (DFS) com os recursos de gestão avançada inspirados pelo `claude-obsidian` (como linting de integridade, log folds, endereços determinísticos estáveis e similaridade semântica local).

---

## 🏗️ Evolução Arquitetural (A Nova Visão v5.0)

Após integrar o design de inteligência local portátil do `claude-obsidian`, o Danger Line v5.0 redefine seus pilares técnicos:

1. **Servidor MCP Multiplataforma Nativo em Python:**
   A comunicação e o processamento de lógica ocorrem em Python puro, eliminando scripts shell (`.sh`) para garantir compatibilidade nativa instantânea no Windows e Linux.

2. **DragonScale Memory Core (Portado para Python):**
   * **Mecanismos de Folds (Compactação):** Agrupa transações cronológicas de escrita em resumos concisos para otimização de busca.
   * **Identificadores de Endereço Estáveis:** Cada página criada recebe um ID persistente em YAML frontmatter (`address: c-NNNNNN`), preservando links mesmo após reestruturações e renomeações.
   * **Busca Semântica por Cosseno:** Detecção de duplicatas em tempo de gravação integrando embeddings rápidos gerados por Ollama local (`nomic-embed-text`).

3. **Linter de Integridade Integrado:**
   Auditoria de integridade da wiki detectando links mortos, notas sem referências (órfãs) e inconsistências de dados YAML em tempo real de forma programática.

4. **Hot Cache de Baixo Custo:**
   Manutenção de uma nota rápida de status recente (`wiki/hot.md`) contendo as últimas alterações, decisões e tópicos ativos para carregar o contexto da IDE em milissegundos sem varrer a base inteira.

---

## Problema que Resolve

A amnésia de contexto em sessões de IA gera gastos excessivos com APIs e perda de tempo ao re-explicar a estrutura do código e decisões anteriores à IDE. O Danger Line garante que cada aprendizado seja documentado de forma estruturada e duradoura no Obsidian, permitindo que a IA da IDE leia e escreva esse "cérebro" de maneira autônoma.

---

## Arquitetura em Alto Nível

```
┌──────────────┐      ┌─────────────────────────────┐      ┌──────────────┐
│  Antigravity │◀────▶│      Danger Line v5.0       │◀────▶│   Obsidian   │
│ (Assistente) │ MCP  │ (Linter + Scorer + Tiling)  │ DFS  │ (Vault Local)│
└──────────────┘      └─────────────────────────────┘      └──────────────┘
```

---

> **Próximos passos**: 
> * Consultar [DOCUMENTO_PROJETO.MD](file:///c:/Users/Adriano/Desktop/PROJETOS/danger_line/documents/DOCUMENTO_PROJETO.MD) para detalhes dos componentes.
> * Consultar [DRAGONSCALE_MCP.MD](file:///c:/Users/Adriano/Desktop/PROJETOS/danger_line/documents/DRAGONSCALE_MCP.MD) para a especificação dos motores de memória.
> * Consultar [FICHA_TECNICA.MD](file:///c:/Users/Adriano/Desktop/PROJETOS/danger_line/documents/FICHA_TECNICA.MD) para a stack técnica e dependências de portabilidade.
