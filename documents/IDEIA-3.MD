# 🛡️ IDEIA 3 — Módulo Sanitizer (Segurança e Privacidade)

## 1. O Problema da Memória Permanente
Ao criar um KB de longo prazo, o maior risco é armazenar acidentalmente dados sensíveis (.env, senhas, dados de clientes). O **Módulo Sanitizer** atua como uma barreira de segurança obrigatória.

## 2. Camadas de Proteção

### Camada 1: Regex Shield (Estática)
- Filtros automáticos baseados em padrões conhecidos:
  - API Keys (AWS, Google, OpenAI).
  - Connection Strings (JDBC, MongoDB, SQL).
  - IPs, Emails e Tokens de Sessão.
- Bloqueio imediato de arquivos em blacklist (`.env`, `.config`, `credentials.json`).

### Camada 2: AI Scrubber (Dinâmica)
- Antes de salvar uma nota no Obsidian, uma IA base faz um scan rápido do texto.
- **Prompt:** "Identifique e remova quaisquer dados reais de banco de dados, senhas ou informações de clientes deste texto, substituindo-os por placeholders genéricos (ex: `<HIDDEN_DB_URL>`)."

### Camada 3: Anonymization (Anonimização)
- Transformação de dados específicos em conceitos genéricos.
- Ex: Em vez de "Bug no banco sigeam_prod", o sistema salva "Bug no banco de produção (Oracle)".

## 3. Fluxo de Segurança
```
Entrada Bruta ──▶ [Regex Filter] ──▶ [AI Scrubber] ──▶ [Placeholder Injection] ──▶ Obsidian
```

## 4. Benefícios
- **Paz de Espírito:** Você pode analisar projetos profissionais sem medo de vazar segredos da empresa para o seu vault pessoal.
- **Compliance:** Mantém o KB limpo e focado em **lógica técnica**, não em dados de produção.

---
> **Status**: Novo módulo prioritário para viabilizar o uso do sistema em projetos profissionais.
