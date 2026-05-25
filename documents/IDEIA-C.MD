# 📋 IDEIA C — Regras Específicas por Projeto (Project Rules via MCP Resources)

## 1. O Problema da Troca de Contexto
O desenvolvedor alterna entre dezenas de projetos (ex: projeto legado em PHP, projeto moderno em Next.js, API em Python). Cada projeto tem "regras da casa" diferentes: estilos de formatação, bibliotecas permitidas, padrões arquiteturais proibidos.
A IA da IDE (Antigravity) costuma esquecer essas regras a cada nova sessão, obrigando o desenvolvedor a lembrar a IA o tempo todo.

## 2. A Solução: Injeção Passiva via MCP Resources
O protocolo MCP possui a funcionalidade de **Resources**, que permite ao servidor expor dados fixos que a IDE lê automaticamente, como um "Aviso no Mural".

### Como Funciona:
1. No Vault do Obsidian, o desenvolvedor cria uma nota dedicada a regras de um projeto. Ex: `/Regras/Regras_Projeto_SIGEAM.md`.
2. Essa nota possui um YAML indicando a qual diretório (Path) do computador ela pertence.
3. O servidor MCP do **Danger Line** fica monitorando a pasta ativa do desenvolvedor. Quando ele detecta que a pasta aberta é `C:\...\SIGEAM`, ele imediatamente expõe o conteúdo daquela nota do Obsidian como um MCP Resource chamado `obsidian://project-rules`.
4. A IDE lê esse Resource silenciosamente em background.

## 3. A Mágica
Da próxima vez que o desenvolvedor pedir *"Crie uma nova rota"*, a IA já analisou o Resource em background e obedece automaticamente às instruções do Obsidian: 
- *"Ah, o Resource do Danger Line disse que neste projeto usamos classes estáticas e não podemos usar axios. Vou gerar o código assim."*

---
> **Status:** Pronta para implementação na Fase 3 do Roadmap. Exigirá a utilização do decorator `@mcp.resource()` do FastMCP e um sistema simples de mapeamento Path <-> Nota.
