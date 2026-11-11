# Sistema Integrado de Gerenciamento Inteligente da Colônia

Sistema em Python que organiza dados da colônia, toma decisões automáticas, prevê geração de energia eólica (regressão linear) e analisa o uso de energia.

## Funcionamento

O sistema está organizado em funções claras:

1. **Organização de dados**: usa dicionários aninhados para representar a hierarquia  
   (sistema energético → solar / eólico) e listas para dados históricos.
2. **Regras de decisão**: aplica condições simples e combinadas, priorizando o suporte à vida.
3. **Previsão**: ajusta uma reta (regressão linear simples) com dados históricos de vento e energia.
4. **Análise de energia**: compara geração e consumo e gera alertas ou sugestões.

## Como executar

```bash
python sistema_colonia.py
```

## Exemplo de entrada e saída

**Entrada (valores internos do sistema):**
- energia = 45
- consumo = 60
- vento = 11
- geração total = 40 (15 solar + 25 eólico)

**Saídas esperadas:**
- Previsão: vento = 11 → energia eólica ≈ 27.5
- Decisão: `ALERTA: energia < 50 → reduzir consumo.`
- Análise: `ALERTA: consumo (60) maior que geração (40) → risco.`

## Estrutura do código

- `criar_estrutura_colonia()`: monta a hierarquia de dados.
- `exibir_estrutura()`: navega e mostra os subsistemas.
- `ajustar_regressao_linear()` + `prever_energia_eolica()`: previsão.
- `tomar_decisao()`: regras de decisão.
- `analisar_uso_energia()`: análise de geração vs consumo.
- `executar_sistema()`: demonstração completa.

## Requisitos

Python 3.8+ (sem bibliotecas externas).

## Autores

Equipe do projeto (disciplina de Estruturas de Dados / Lógica de Programação).
