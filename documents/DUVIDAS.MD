# ❓ DÚVIDAS — DANGER LINE

## 1. Dúvidas sobre a Remodelagem

### Q-01: Por que remover a pasta `danger_line/` local dos projetos?
**R**: Porque o foco agora é **Zero Footprint**. Centralizar tudo no Obsidian facilita a busca global, o backup e evita que arquivos de metadados "sujem" os repositórios de código. O Obsidian já é o local de organização, então faz sentido que ele seja o repositório físico do conhecimento.

### Q-02: Como o sistema identifica um projeto sem uma pasta local?
**R**: O sistema utiliza o **Path Absoluto** ou o nome do repositório como identificador único. No Obsidian, haverá um mapeamento entre o Path do projeto e seu respectivo Project Card.

### Q-03: Qual a vantagem de separar em Módulo MCP e Módulo Obsidian?
**R**: **Modularidade e Escalabilidade**. Se amanhã quisermos trocar o Obsidian pelo Notion ou outra ferramenta, basta trocar o Módulo Obsidian. Se quisermos criar uma interface Slack em vez de MCP, basta adicionar um Módulo Slack. O Core permanece intacto.

### Q-04: Como será a integração com Voz?
**R**: O sistema terá uma API interna (Core) que receberá comandos. O módulo de voz converterá fala em texto e chamará as funções do Core, permitindo, por exemplo, perguntar: "Danger Line, qual o padrão de autenticação do projeto X?" e receber a resposta lida do Obsidian.

---

## 2. Dúvidas Técnicas (Nova Fase)

### Q-05: Como o MCP Resource será usado?
**R**: Os resources serão usados para expor dados dinâmicos. Por exemplo, podemos ter um resource chamado `obsidian://current-project-rules` que a IA lê sempre que entra em um projeto, garantindo que ela siga os padrões documentados no Obsidian sem que o usuário precise explicar.

### Q-06: O sistema ainda economiza tokens?
**R**: Sim, de forma mais inteligente. Em vez de enviar o código bruto para a IA analisar, enviamos o **conhecimento já destilado** do Obsidian. Isso é muito mais denso e consome menos tokens do que código bruto redundante.

### Q-07: Precisamos de um servidor rodando?
**R**: Para o MCP, o Antigravity inicia o processo automaticamente. Para futuras integrações (como Voz ou Web), um pequeno servidor local (FastAPI) pode ser necessário como módulo de orquestração.

---

## 3. Próximos Passos de Decisão

- [ ] Definir a estrutura exata de pastas dentro do Vault do Obsidian.
- [ ] Escolher a biblioteca de reconhecimento de voz para o módulo futuro.
- [ ] Mapear as 5 ferramentas iniciais do Módulo MCP.
- [ ] Criar o template padrão do Project Card v3.
