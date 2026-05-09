# 🔴 DANGER LINE — Resumo do Projeto

## Visão Geral

O **Danger Line** evoluiu para ser um sistema de gerenciamento de conhecimento (Knowledge Base - KB) profundamente integrado ao **Obsidian** e operando primariamente via **MCP (Model Context Protocol)**. O foco central é transformar a experiência de desenvolvimento com IA, utilizando o Obsidian como cérebro central para armazenar padrões, bugs conhecidos e arquiteturas de projetos.

O sistema atua como uma camada de inteligência entre o desenvolvedor (usando Antigravity/Claude/Gemini) e a base de código, otimizando o consumo de tokens e potencializando a precisão das IAs de alta performance através de um contexto refinado e histórico.

---

## Estratégia Principal: KB + Obsidian + MCP

1.  **MCP-First**: O uso prioritário é como ferramenta MCP dentro do Antigravity, permitindo que a IA consulte e alimente a base de conhecimento de forma fluida.
2.  **Cérebro no Obsidian**: Todo o conhecimento é sistematizado e armazenado dentro do Obsidian, seguindo a lógica KB. Não há mais poluição de pastas locais nos projetos.
3.  **Metodologia KB**: Implementação profunda do método de Knowledge Base para capturar a essência de cada projeto, padrões de código e resoluções de problemas.
4.  **Arquitetura Modular**: Sistema desenhado para ser escalável, permitindo futuras integrações (ex: reconhecimento de voz) de forma plug-and-play.

---

## Problema que Resolve

Desenvolvedores perdem eficiência e dinheiro com:
- Contexto repetitivo enviado para IAs pagas.
- Esquecimento de padrões de arquitetura e soluções de bugs passados.
- Fragmentação de conhecimento entre diferentes projetos.
- Dificuldade em manter uma documentação viva e útil para a própria IA.

## Solução Proposta

Um **Ecossistema de Inteligência** que:
1.  **Centraliza** o conhecimento técnico no Obsidian.
2.  **Automatiza** a criação de Project Cards e wikis de arquitetura.
3.  **Otimiza** prompts usando o histórico de aprendizado do sistema.
4.  **Escala** conforme o uso, tornando a IA "mais inteligente" a cada interação com o projeto.

---

## Arquitetura em Alto Nível

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Antigravity │◀────▶│  Danger Line │◀────▶│   Obsidian   │
│     (IA)     │ MCP  │  (Core/KB)   │ File │ (Vault/Wiki) │
└──────────────┘      └──────────────┘      └──────────────┘
                             ▲
                             │ Plugins/Módulos
                             ▼
                    ┌────────────────┐
                    │ Futuros (Voz,  │
                    │   Dashboard)   │
                    └────────────────┘
```

## Modalidades de Uso

| Modalidade | Descrição | Status |
|------------|-----------|--------|
| **MCP Server** | Integração total com Antigravity; ferramenta principal de interação. | **Prioridade P0** |
| **CLI Multiplat.** | Interface de comando para gestão administrativa e automações. | **Prioridade P1** |

---

## Tecnologias e Módulos

O sistema é dividido em dois grandes módulos centrais:
- **Módulo MCP**: Gerencia ferramentas, recursos e a comunicação com a IA.
- **Módulo Obsidian**: Controla a leitura, escrita e estruturação do Knowledge Base no vault.

---

> **Próximo passo**: Consultar `DOCUMENTO_PROJETO.MD` para detalhes da nova arquitetura modular e `FICHA_TECNICA.MD` para especificações dos módulos.
