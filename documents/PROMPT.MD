# 📋 PROMPT REFINADO — DANGER LINE v2

> **Nota**: Este é o prompt original do usuário, refinado para maior clareza e estruturação. Sem interferências de análise externa. Pronto para ser utilizado em outra IA.

---

## Contexto

Estou desenvolvendo um sistema chamado **Danger Line** — um assistente administrativo e de desenvolvimento que utiliza uma IA gratuita como base para análise, busca e resumo de código-fonte, otimizando contexto para ser consumido por uma IA paga de alta performance.

O objetivo principal é **economizar tokens da IA paga**, delegando tarefas simples para a IA gratuita e escalando apenas o necessário.

Tenho um protótipo anterior em Python que usa Ollama + CLI + Obsidian, mas preciso recomeçar com uma arquitetura mais robusta.

---

## Requisitos do Sistema

### REQ-1: IA Base Gratuita
- O sistema deve utilizar um modelo de IA gratuito como motor principal
- Opções em ordem de prioridade: **Groq API** (free tier), **Gemini Flash** (free tier), **LLM local via Ollama**
- A LLM local (gemma4:e4b) é muito limitada em contexto (~4K tokens) — deve ser usada apenas como fallback offline
- Implementar fallback automático entre providers
- **Explorar**: É possível integrar diretamente com o Antigravity IDE via MCP? Se sim, podemos usar o Gemini como IA potente sem custo adicional

### REQ-2: Workspace Direcionado + MCP Server
- O sistema deve ser direcionado a uma pasta/projeto específico
- **Opção A (preferida)**: Implementar como MCP Server (Model Context Protocol) para integração nativa com Antigravity/Gemini CLI
- **Opção B (fallback)**: Implementar como CLI standalone linkado a um workspace
- Investigar viabilidade de transformar em MCP Server e usá-lo como assistente literal dentro do Antigravity

### REQ-3: Análise e Resumo com Armazenamento
- O sistema deve analisar código-fonte e gerar resumos em **dois formatos**:
  - **Para IA**: 100% otimizado para consumo por IA — em inglês, com prompt negativo, structured data, seguindo melhores práticas de prompting
  - **Para Humano**: Documentação técnica em Markdown (PT-BR) — padrões de documentos de arquitetura, diagramas, escrita técnica
- Armazenamento temporário (cache) e permanente (Markdown files)
- Compatibilidade com Obsidian (opcional) para organização em vault
- Explorar se Obsidian é a melhor opção ou se há alternativas melhores

### REQ-4: Sistema de Classificação por Dificuldade (Estrelas)
- A IA base deve classificar cada problema em **3 níveis**:
  - **1★ Simples**: IA base resolve sozinha (erros de sintaxe, config, typos)
  - **2★ Médio**: IA base elabora solução + solicita consentimento do usuário para escalar para IA potente
  - **3★ Complexo**: Escala automaticamente para IA potente com contexto otimizado
- **Importante**: A IA base NÃO para de utilizar a IA potente para 1-2★. Ela:
  1. Analisa e elabora a solução localmente
  2. Detalha a solução para a IA potente
  3. A IA potente emite um **alvará** (aprovação + correções se necessário)
  4. Isso acontece em batch, não em tempo real, para economizar tokens
- O uso da IA potente é terceirizado (via meu acesso ao Antigravity/API)

### REQ-5: Painel de Controle via Terminal
- Dashboard no terminal mostrando:
  - **% de tokens economizados** vs uso direto da IA potente
  - **Tokens gastos** na IA base vs IA potente
  - **Contexto utilizado** e métricas de uso
  - **Análise da IA potente** sobre qualidade das análises da IA base + sugestões de melhoria
  - Distribuição de problemas por nível de estrela

---

## Restrições Técnicas

- **Linguagem**: Python 3.11+
- **LLM Local**: gemma4:e4b via Ollama — muito limitada, janela de contexto pequena
- **Orçamento**: Zero para IA base (usar tiers gratuitos)
- **Plataforma**: Windows 11
- **IDE**: Antigravity (Google DeepMind)

---

## Deliverables Solicitados

1. Análise completa do projeto existente
2. Documentação técnica com diagramas de arquitetura
3. Plano de implementação dividido em fases
4. Testes definidos por caso de uso (TDD)
5. Respostas para dúvidas técnicas sobre Docker, LLM local, MCP, arquitetura

---

## Dúvidas para a IA

1. Docker: devemos usar? Em quais cenários? Qual a melhor alternativa?
2. LLM Local: como usar a gemma4 de forma viável dado o contexto limitado?
3. Arquitetura: qual o melhor padrão arquitetural para este sistema?
4. MCP: como integrar com Antigravity como agente/assistente?
5. Projeto antigo: o que pode ser reaproveitado?
6. Qual nível técnico do meu prompt e como melhorar?
