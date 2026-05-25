# 🧠 IDEIA 1 — Obsidian como Knowledge Engine Nativo

## 1. O Vault como Banco de Dados Vivo
O Obsidian é o repositório central e absoluto de inteligência do Danger Line. A integração, no entanto, passa a ser 100% via sistema de arquivos local (DFS), abandonando APIs e dependências que exijam que o aplicativo do Obsidian esteja rodando.

## 2. A Nova Estrutura Unificada (Sem Stacks)
Para simplificar e reduzir a fragmentação de conhecimento (já que não usamos mais "context switchers" entre Backend e Frontend), a organização do Obsidian passa a se focar em **domínios de problema e abstração** em vez de stacks tecnológicas.

### Estrutura de Diretórios Recomendada
- `🧩 Padrões/`: Princípios de Clean Code, arquitetura de software unificada, abstrações. (Ex: "Como fazemos injeção de dependência neste projeto").
- `🐛 BugTracker/`: Repositório global de erros e resoluções, classificados por tags do Obsidian.
- `🚀 Funcionalidades/`: Especificações técnicas (Specs) de regras de negócio e fluxos.
- `📚 Playbooks/`: Manuais e guias passo a passo para fazer deploy, configurar ambiente, etc.

## 3. O Poder do Dataview e Metadados
Embora não nos comuniquemos via API, ainda utilizamos o formato rico do Obsidian. O Módulo Obsidian do Danger Line escreverá as notas contendo Frontmatter YAML e `#tags` muito precisas.
A IA da IDE poderá ler e cruzar essas informações no diretório. E para o usuário humano, plugins do Obsidian como o **Dataview** vão ler esses metadados gerados pela IA e construir dashboards fantásticos dentro do próprio aplicativo Obsidian.

## 4. Integração com o Core
O Módulo Obsidian (`src/modules/obsidian/`) implementa classes de controle padrão para abstrair a leitura e formatação dos wikilinks (`[[arquivo]]`). Isso garante que a IA não quebre a "saúde" da sua wiki ao salvar novos arquivos.
