"""
Módulo de Contratos de Dados

Este módulo define os formatos padronizados de entrada e saída utilizados pelo workflow.
Baseado no documento `docs/contrato.md`.
"""

from typing import List, Literal, TypedDict, Optional, Dict, Any

# ==============================================================================
# Tipos Básicos
# ==============================================================================

CategoriaPermitida = Literal["estrutura", "referencias", "ortografia"]

# ==============================================================================
# Contrato de Entrada
# ==============================================================================

class EntradaRequest(TypedDict):
    """
    Contrato de Entrada
    Todo documento enviado ao sistema deve seguir esta estrutura.
    """
    arquivo: str
    categorias: List[CategoriaPermitida]

# ==============================================================================
# Contrato da Etapa de Extração
# ==============================================================================

class ExtracaoSucesso(TypedDict):
    texto_extraido: str
    paginas: int
    status: Literal["sucesso"]

class ExtracaoErro(TypedDict):
    status: Literal["erro"]
    codigo: str
    mensagem: str

# ExtracaoOutput pode ser sucesso ou erro
ExtracaoOutput = ExtracaoSucesso | ExtracaoErro

# ==============================================================================
# Contratos das Ferramentas
# ==============================================================================

class EstruturaOutput(TypedDict, total=False):
    """Contrato da Ferramenta verificar_estrutura"""
    categoria: Literal["estrutura"]
    introducao: bool
    desenvolvimento: bool
    conclusao: bool
    # Em caso de falha:
    status: str
    motivo: str
    codigo: str

class ReferenciasOutput(TypedDict, total=False):
    """Contrato da Ferramenta verificar_referencias"""
    categoria: Literal["referencias"]
    quantidade: int
    possui_secao: bool
    # Em caso de ausência/erro:
    status: str
    motivo: str
    codigo: str

class OrtografiaOutput(TypedDict, total=False):
    """Contrato da Ferramenta verificar_ortografia"""
    categoria: Literal["ortografia"]
    erros: int
    # Em caso de erro:
    status: str
    mensagem: str
    codigo: str

# ==============================================================================
# Contrato de Consolidação (Etapa 5)
# ==============================================================================

class ConsolidacaoOutput(TypedDict, total=False):
    """Resultados produzidos pelas ferramentas executadas."""
    estrutura: EstruturaOutput
    referencias: ReferenciasOutput
    ortografia: OrtografiaOutput

# ==============================================================================
# Contrato da Saída Final (Etapa 7)
# ==============================================================================

class RelatorioFinal(TypedDict, total=False):
    """
    A resposta final do sistema (Relatório Final).
    Pode omitir as chaves das categorias se não tiverem sido solicitadas.
    """
    status_final: Literal["necessita_revisao", "aprovado_com_ressalvas", "reprovado", "erro"]
    estrutura: EstruturaOutput
    referencias: ReferenciasOutput
    ortografia: OrtografiaOutput
    validacao: bool
    # Motivo pode existir se a validação falhar
    motivo: str
