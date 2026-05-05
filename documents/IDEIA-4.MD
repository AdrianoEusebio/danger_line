# 💡 IDEIA 4 — Sistema de Classificação por Estrelas e Delegação

## Conceito

A IA base classifica cada problema por **dificuldade (1-3★)** e decide a rota:

- **1★ Simples**: IA base resolve sozinha
- **2★ Médio**: IA base elabora + pede consentimento para escalar
- **3★ Complexo**: Escala direto para IA potente

**Regra do Alvará**: Mesmo para 1-2★, soluções são acumuladas em batch e revisadas pela IA potente periodicamente.

> **Integração KB (Ideia 6)**: O Classifier agora consulta o `wiki/bugs/` e `wiki/patterns/` antes de classificar. Se o KB já tem solução para um pattern similar, pode **reclassificar de 3★ para 1★**. Soluções resolvidas alimentam o KB via Filed Back.

## Fluxos por Nível

### 1★ — Simples
```
Problema → IA Base (1★) → Resolve → Buffer de Revisão → [Batch] IA Potente aprova
```
Exemplos: erros de sintaxe, imports faltando, typos, config

### 2★ — Intermediário
```
Problema → IA Base (2★) → Elabora solução → Pergunta: "Escalar? (Y/n)"
  ├─ [Y] → Contexto otimizado → IA Potente
  └─ [N] → Apresenta solução com disclaimer → Buffer de Revisão
```
Exemplos: bugs de lógica, refatoração, integração

### 3★ — Complexo
```
Problema → IA Base (3★) → Gera Super-Prompt → IA Potente resolve
```
Exemplos: arquitetura, performance, segurança, multi-módulo

## Passos Técnicos

### Passo 1: Classifier Engine
```python
class Difficulty(IntEnum):
    SIMPLE = 1    # ⭐
    MODERATE = 2  # ⭐⭐  
    COMPLEX = 3   # ⭐⭐⭐

class DifficultyClassifier:
    PROMPT = """Classify difficulty as 1(simple), 2(moderate), 3(complex).
    1★: syntax, imports, typos, config, OR known pattern in wiki
    2★: logic bugs, small refactors, <3 files
    3★: architecture, performance, security, multi-module
    
    IMPORTANT: If WIKI_CONTEXT contains a similar solved bug, downgrade difficulty.
    
    RESPOND JSON: {"difficulty": N, "confidence": 0.0-1.0, "reasoning": "...", "category": "...", "wiki_match": "article_name or null"}"""
    
    async def classify(self, problem, context="", wiki_context="") -> Classification:
        prompt = f"PROBLEM: {problem}\nCODE CONTEXT: {context}"
        if wiki_context:
            prompt += f"\nWIKI_CONTEXT (known bugs/patterns):\n{wiki_context}"
        response = await self.provider.complete(prompt=prompt, system=self.PROMPT)
        return Classification(**json.loads(response))
```

### Passo 2: Orquestrador de Decisão
```python
class AgentOrchestrator:
    async def handle_problem(self, problem, files=[]):
        context = await self.analyzer.analyze_files(files)
        
        # KB Query: consultar wiki antes de classificar
        wiki_context = await self.qa_engine.query(
            f"Known bugs or patterns related to: {problem}"
        )
        
        classification = await self.classifier.classify(
            problem, context, wiki_context=wiki_context.answer
        )
        
        match classification.difficulty:
            case Difficulty.SIMPLE:   return await self._handle_simple(problem, context)
            case Difficulty.MODERATE: return await self._handle_moderate(problem, context)
            case Difficulty.COMPLEX:  return await self._handle_complex(problem, context)
```

### Passo 3: Review Buffer (Alvará)
```python
class ReviewBuffer:
    """Acumula soluções para revisão em batch pela IA potente."""
    def __init__(self):
        self.pending: list[PendingReview] = []
    
    def get_batch_prompt(self) -> str:
        prompt = "### BATCH REVIEW ###\nReview these base AI solutions. APPROVE or correct each:\n\n"
        for i, r in enumerate(self.pending):
            prompt += f"--- ITEM {i+1} ({r.difficulty}★) ---\nProblem: {r.problem}\nSolution: {r.solution}\n\n"
        return prompt
```

### Passo 4: Calibração com Exemplos
Manter arquivo de exemplos para few-shot learning do classifier:
```json
[
    {"problem": "SyntaxError: unexpected EOF", "difficulty": 1},
    {"problem": "Button onClick not firing", "difficulty": 2},
    {"problem": "API 500 on concurrent requests", "difficulty": 3}
]
```

### Passo 5: Métricas de Precisão
Rastrear acerto da classificação via feedback da IA potente no alvará.

---

## O Alvará em Detalhe

1. Soluções 1-2★ acumulam no buffer
2. Periodicamente (ou sob demanda), buffer vai em batch para IA potente
3. IA potente emite: aprovação + correções + sugestões
4. Correções aplicadas retroativamente
5. Feedback calibra o classifier para futuras classificações
6. **Filed Back**: Soluções aprovadas vão para `raw/solutions/` → compiladas no wiki
7. **Reclassificação**: Se o wiki acumula soluções para patterns similares, futuros problemas do mesmo tipo são automaticamente classificados como 1★
