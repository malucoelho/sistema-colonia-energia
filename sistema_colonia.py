"""
Sistema Integrado de Gerenciamento Inteligente da Colônia
==========================================================
Organiza dados, toma decisões automáticas, prevê energia eólica
e analisa o uso de energia da colônia.

Estrutura:
- Dados organizados em dicionários (chave-valor) e listas
- Hierarquia de sistemas (energético → solar / eólico)
- Funções separadas para lógica, decisões e previsão
"""

from typing import Dict, List, Tuple, Any


# ==================== ORGANIZAÇÃO DE DADOS ====================

def criar_estrutura_colonia() -> Dict[str, Any]:
    """
    Cria a estrutura hierárquica da colônia usando dicionários aninhados.
    Representa sistemas e subsistemas (ex.: sistema energético → solar / eólico).
    """
    colonia = {
        "energia": {
            "nivel_atual": 45.0,          # energia disponível (%)
            "reserva": 20.0,              # energia em reserva
            "sistemas": {
                "solar": {
                    "capacidade": 30.0,
                    "geracao_atual": 15.0
                },
                "eolico": {
                    "capacidade": 40.0,
                    "geracao_atual": 25.0
                }
            }
        },
        "consumo": {
            "total": 60.0,
            "suporte_vida": 30.0,         # prioridade máxima
            "nao_essencial": 30.0
        },
        "clima": {
            "vento": 10.0,                # velocidade do vento (m/s)
            "temperatura": 22.0
        }
    }
    return colonia


def obter_geracao_total(colonia: Dict[str, Any]) -> float:
    """Navega na hierarquia e soma a geração dos subsistemas energéticos."""
    sistemas = colonia["energia"]["sistemas"]
    return sum(s["geracao_atual"] for s in sistemas.values())


def exibir_estrutura(colonia: Dict[str, Any], nivel: int = 0) -> None:
    """Exibe a estrutura hierárquica de forma indentada (navegação)."""
    for chave, valor in colonia.items():
        prefixo = "  " * nivel
        if isinstance(valor, dict):
            print(f"{prefixo}{chave}:")
            exibir_estrutura(valor, nivel + 1)
        else:
            print(f"{prefixo}{chave}: {valor}")


# ==================== PREVISÃO (REGRESSÃO LINEAR SIMPLES) ====================

def ajustar_regressao_linear(x: List[float], y: List[float]) -> Tuple[float, float]:
    """
    Ajusta uma reta simples (regressão linear) usando apenas Python puro.
    Retorna (inclinação, intercepto).
    Fórmula: slope = Σ((xi - x̄)(yi - ȳ)) / Σ((xi - x̄)²)
             intercept = ȳ - slope * x̄
    """
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Listas devem ter o mesmo tamanho e pelo menos 2 pontos.")

    n = len(x)
    x_media = sum(x) / n
    y_media = sum(y) / n

    numerador = sum((xi - x_media) * (yi - y_media) for xi, yi in zip(x, y))
    denominador = sum((xi - x_media) ** 2 for xi in x)

    if denominador == 0:
        raise ValueError("Não é possível ajustar reta (variância zero).")

    slope = numerador / denominador
    intercept = y_media - slope * x_media
    return slope, intercept


def prever_energia_eolica(vento: float, 
                          vento_hist: List[float] = None,
                          energia_hist: List[float] = None) -> float:
    """
    Prevê a energia eólica gerada a partir da velocidade do vento,
    usando regressão linear nos dados históricos.
    """
    if vento_hist is None:
        # Dados de exemplo do enunciado
        vento_hist = [8.0, 10.0, 12.0]
        energia_hist = [20.0, 25.0, 30.0]

    slope, intercept = ajustar_regressao_linear(vento_hist, energia_hist)
    previsao = slope * vento + intercept
    return round(previsao, 2)


# ==================== REGRAS DE DECISÃO ====================

def tomar_decisao(energia: float, consumo: float, 
                  suporte_vida: float = 30.0) -> str:
    """
    Aplica regras de decisão simples e combinadas.
    Prioriza o suporte à vida e gera uma ação clara.
    """
    # Prioridade máxima: suporte à vida sempre ligado
    if energia < suporte_vida:
        return "ALERTA CRÍTICO: energia insuficiente para suporte à vida! Reduzir consumo imediatamente."

    # Regra simples
    if energia < 50:
        # Combinação de condições
        if consumo > 60:
            return "ALERTA: energia baixa E consumo alto → ativar modo economia (desligar sistemas não essenciais)."
        else:
            return "ALERTA: energia < 50 → reduzir consumo."

    # Análise de equilíbrio
    if consumo > energia:
        return "ALERTA: consumo maior que energia disponível → risco de apagão."
    elif energia - consumo > 30:
        return "SUGESTÃO: armazenar energia excedente na reserva."
    else:
        return "STATUS: operação normal. Manter sistemas atuais."


# ==================== ANÁLISE DE ENERGIA ====================

def analisar_uso_energia(geracao: float, consumo: float) -> str:
    """
    Compara geração e consumo e gera uma ação simples.
    """
    if consumo > geracao:
        return f"ALERTA: consumo ({consumo}) maior que geração ({geracao}) → risco."
    elif geracao > consumo * 1.3:  # excesso significativo
        return f"SUGESTÃO: armazenar energia excedente (geração {geracao} > consumo {consumo})."
    else:
        return f"STATUS: equilíbrio adequado (geração {geracao}, consumo {consumo})."


# ==================== FUNÇÃO PRINCIPAL (DEMONSTRAÇÃO) ====================

def executar_sistema():
    """Executa o sistema completo com exemplos de entrada e saída."""
    print("=" * 60)
    print("SISTEMA INTEGRADO DA COLÔNIA")
    print("=" * 60)

    # 1. Organizar dados
    print("\n1. ORGANIZAÇÃO DOS DADOS (estrutura hierárquica):")
    colonia = criar_estrutura_colonia()
    exibir_estrutura(colonia)

    geracao_total = obter_geracao_total(colonia)
    print(f"\nGeração total calculada (navegando subsistemas): {geracao_total}")

    # 2. Previsão
    print("\n2. PREVISÃO DE ENERGIA EÓLICA (regressão linear):")
    vento_teste = 11.0
    previsao = prever_energia_eolica(vento_teste)
    print(f"Entrada: vento = {vento_teste}")
    print(f"Saída: previsão de energia ≈ {previsao}")

    # 3. Decisão
    print("\n3. TOMADA DE DECISÃO AUTOMÁTICA:")
    energia = colonia["energia"]["nivel_atual"]
    consumo = colonia["consumo"]["total"]
    decisao = tomar_decisao(energia, consumo)
    print(f"Entrada: energia = {energia}, consumo = {consumo}")
    print(f"Saída: {decisao}")

    # 4. Análise de energia
    print("\n4. ANÁLISE DO USO DE ENERGIA:")
    analise = analisar_uso_energia(geracao_total, consumo)
    print(f"Entrada: geração = {geracao_total}, consumo = {consumo}")
    print(f"Saída: {analise}")

    print("\n" + "=" * 60)
    print("Sistema executado com sucesso.")
    print("=" * 60)


if __name__ == "__main__":
    executar_sistema()
