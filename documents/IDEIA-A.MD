# 🏷️ IDEIA A — Organização por Tags Semânticas (Fim das Pastas Rígidas)

## 1. O Paradigma Atual vs O Novo Paradigma
Anteriormente, o sistema tentava forçar o conhecimento em "caixas" engessadas, como `/Backend`, `/Frontend`, `/Infra`. Isso gerava atrito: onde colocar um arquivo que fala sobre o deploy (Infra) de uma API (Backend)?

**A nova abordagem:** Adoção de um modelo "Flat-ish" (Plano) com o uso massivo de **Propriedades YAML (Frontmatter) e Tags Semânticas**.

## 2. Como Funciona
O Obsidian é excepcionalmente poderoso para cruzar dados usando tags. Em vez de criar pastas profundas, o Danger Line escreverá os manuais e padrões em uma pasta central (ex: `/Notas_Tecnicas`) e injetará metadados ricos:

```yaml
---
tipo: playbook
tecnologias: [nodejs, react, aws]
dominio: autenticacao
tags:
  - backend
  - frontend
  - security
---
```

## 3. Benefícios
- **Busca Multidimensional:** A ferramenta MCP `query_kb` poderá receber argumentos flexíveis. A IA pode pedir ao Danger Line: *"Me dê todas as notas que tenham as tags `#security` e `#backend`"*.
- **Descoberta:** O desenvolvedor ganha uma visão unificada no aplicativo do Obsidian através do plugin **Dataview**, podendo gerar tabelas dinâmicas independentes da pasta onde o arquivo mora.
- **Flexibilidade:** Se uma tecnologia mudar, basta atualizar a propriedade YAML da nota, sem precisar mover o arquivo fisicamente pelo disco.

---
> **Status:** Pronta para implementação. A classe `MarkdownBuilder` deverá forçar a injeção dessas propriedades em todas as criações de conhecimento.
