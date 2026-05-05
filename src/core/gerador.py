class GeradorDePrompt:
    @staticmethod
    def criar_super_prompt(projeto, arquivo_erro, conteudo_codigo, dependencias, erro_log):
        """Constrói um Super-Prompt estruturado para análise avançada."""
        prompt = f"""### ARQUITETURA DE CONTEXTO - LIBRARIAN-AI ###

Você é uma IA Senior Full-Stack e Engenheiro de Software. Seu objetivo é analisar o erro abaixo e propor uma solução considerando todo o contexto fornecido.

---
#### 1. PROJETO: {projeto}
#### 2. ARQUIVO COM ERRO: {arquivo_erro}

#### 3. LOG DE ERRO / DESCRIÇÃO:
```text
{erro_log}
```

#### 4. DEPENDÊNCIAS DETECTADAS:
- {', '.join(dependencias) if dependencias else 'Nenhuma detectada'}

#### 5. CONTEÚDO DO CÓDIGO FONTE:
```python
{conteudo_codigo}
```

---
#### INSTRUÇÕES PARA A IA PERFORMANCE:
- Analise se o erro é sintático ou lógico.
- Verifique se o problema está em alguma das dependências citadas.
- Proponha o código corrigido e explique o porquê da mudança.
- Se houver implicações de arquitetura, mencione-as.

[FIM DO CONTEXTO LIBRARIAN-AI]
"""
        return prompt
