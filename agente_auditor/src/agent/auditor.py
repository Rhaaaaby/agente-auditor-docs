"""
Orquestrador do Agente Auditor de Documentos

Este módulo é responsável por coordenar o workflow agêntico completo,
conectando todas as etapas desde a extração de texto até a geração
do relatório final e validação.
"""

import logging
from typing import Dict, Any

from models.contratos import EntradaRequest, RelatorioFinal
from tools.pdf_extractor import extrair_pdf
from tools.estrutura import verificar_estrutura
from tools.referencias import validar_referencias as verificar_referencias
from tools.ortografia import verificar_ortografia
from validators.validator import validar_resultados

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgenteAuditor:
    """
    Agente principal que executa o workflow de auditoria de documentos.
    """
    
    def __init__(self):
        # Mapeamento de categorias para as funções das ferramentas
        self.ferramentas = {
            "estrutura": verificar_estrutura,
            "referencias": verificar_referencias,
            "ortografia": verificar_ortografia
        }
        
    def executar_auditoria(self, request: EntradaRequest) -> RelatorioFinal:
        """
        Executa o fluxo completo (Etapas 1 a 7) baseado no pedido.
        
        Args:
            request (EntradaRequest): Objeto de requisição com arquivo e categorias.
            
        Returns:
            RelatorioFinal: Relatório final do agente.
        """
        logger.info(f"Iniciando auditoria para arquivo: {request['arquivo']}")
        
        # Etapa 1: Validação da Entrada
        if not request.get("arquivo") or not request.get("categorias"):
            return {
                "status_final": "erro",
                "validacao": False,
                "motivo": "Entrada inválida: arquivo ou categorias ausentes."
            }
            
        categorias_solicitadas = request["categorias"]
        
        # Etapa 2: Extração de Texto
        extracao_result = extrair_pdf(request["arquivo"])
        if not extracao_result.get("sucesso"):
            logger.error("Falha na extração de texto do PDF")
            return {
                "status_final": "erro",
                "validacao": False,
                "motivo": extracao_result.get("mensagem", "Falha na extração do texto.")
            }
            
        texto = extracao_result.get("texto_extraido", "")
        if not texto.strip():
            return {
                "status_final": "erro",
                "validacao": False,
                "motivo": "Texto extraído está vazio ou insuficiente."
            }
            
        # Etapa 3 e 4: Planejamento e Execução das Ferramentas
        resultados_ferramentas: Dict[str, Any] = {}
        for categoria in categorias_solicitadas:
            if categoria in self.ferramentas:
                logger.info(f"Executando ferramenta para a categoria: {categoria}")
                try:
                    ferramenta_fn = self.ferramentas[categoria]
                    resultado = ferramenta_fn(texto)
                    resultados_ferramentas[categoria] = resultado
                except Exception as e:
                    logger.error(f"Erro ao executar ferramenta {categoria}: {str(e)}")
                    resultados_ferramentas[categoria] = {
                        "categoria": categoria,
                        "status": "erro",
                        "mensagem": f"Erro interno na ferramenta: {str(e)}"
                    }
            else:
                logger.warning(f"Categoria '{categoria}' não reconhecida.")
                resultados_ferramentas[categoria] = {
                    "categoria": categoria,
                    "status": "erro",
                    "mensagem": "Categoria de análise não implementada."
                }
                
        # Etapa 5 e 6: Consolidação e Validação
        resultado_validacao = validar_resultados(categorias_solicitadas, resultados_ferramentas)
        
        # Etapa 7: Relatório Final
        relatorio_final: RelatorioFinal = {
            "validacao": resultado_validacao.get("validacao", False)
        }
        
        # Copiar os resultados das ferramentas para o relatorio
        if "estrutura" in resultados_ferramentas:
            relatorio_final["estrutura"] = resultados_ferramentas["estrutura"]
        if "referencias" in resultados_ferramentas:
            relatorio_final["referencias"] = resultados_ferramentas["referencias"]
        if "ortografia" in resultados_ferramentas:
            relatorio_final["ortografia"] = resultados_ferramentas["ortografia"]
            
        # Determinar status_final com base na validação
        if not relatorio_final["validacao"]:
            relatorio_final["status_final"] = "necessita_revisao"
            relatorio_final["motivo"] = resultado_validacao.get("motivo", "Validação falhou sem motivo especificado.")
        else:
            relatorio_final["status_final"] = "aprovado_com_ressalvas"  # Padrão seguro, IA não dá aprovação total
            
        logger.info("Auditoria finalizada com sucesso.")
        return relatorio_final

# ==============================================================================
# Exemplo de uso
# ==============================================================================
if __name__ == "__main__":
    agente = AgenteAuditor()
    
    # Criar um mock request - num cenário real, este arquivo deve existir
    mock_request = EntradaRequest(
        arquivo="arquivo_teste_inexistente.pdf",
        categorias=["estrutura", "referencias", "ortografia"]
    )
    
    resultado = agente.executar_auditoria(mock_request)
    import json
    print("\nResultado do Workflow:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
