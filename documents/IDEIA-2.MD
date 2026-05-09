# 🧠 IDEIA 2 — Nova Modelagem de Captura KB

## 1. Do Resumo ao Modelo Mental
O Danger Line abandona a ideia de "resumos de arquivos" e "classificação por estrelas". O novo foco é capturar **Modelos Mentais Acionáveis** que ajudam o desenvolvedor e a IA a resolverem problemas futuros.

## 2. Tipos de Notas (A tríade de Valor)
A captura é filtrada em três formatos atômicos:

### A. Specs (Especificações Técnicas)
- **O que é:** O mapa de como um sistema funciona.
- **Exemplo:** "O fluxo de autenticação usa JWT com refresh token via Redis".
- **Valor:** Evita que a IA precise reanalisar o código de auth toda vez.

### B. Playbooks (Guias de Solução)
- **O que é:** Scripts de resolução para problemas recorrentes.
- **Exemplo:** "Para adicionar um novo campo no formulário X, siga estes passos no backend e frontend".
- **Valor:** Transforma você em um "desenvolvedor sênior" do seu próprio código.

### C. Dívidas e Riscos
- **O que é:** Notas sobre gargalos e áreas que precisam de refatoração.
- **Exemplo:** "Este loop no arquivo Y é ineficiente para mais de 1000 registros".
- **Valor:** Cria um roadmap natural de melhoria para o projeto.

## 3. O Processo de Captura
1.  **Observação:** O sistema monitora a sessão de dev (erros, perguntas, soluções).
2.  **Destilação:** A IA base identifica se o que aconteceu é um novo `Pattern`, uma `Spec` ou um `Playbook`.
3.  **Sanitização:** O **Módulo Sanitizer** (IDEIA-3) remove dados sensíveis.
4.  **Persistência:** A nota é salva no contexto correto do Obsidian (IDEIA-4).

---
> **Status**: Refatorado para foco total em utilidade prática e agnostismo de IA.
