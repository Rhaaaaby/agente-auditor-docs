"""
Módulo de Validação do Relatório

Este módulo implementa a Etapa 6 do workflow: Validação.
Responsabilidades:
- Comparar categorias solicitadas com categorias processadas;
- Detectar falhas de execução nas ferramentas;
- Confirmar integridade do relatório.
"""

import logging
from typing import Dict, List, Any

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidadorRelatorio:
    """
    Classe responsável pela validação da integridade dos resultados do workflow.
    """
    
    def __init__(self, categorias_solicitadas: List[str], resultados_processados: Dict[str, Any]):
        """
        Inicializa o validador.
        
        Args:
            categorias_solicitadas (List[str]): Lista de categorias que o usuário selecionou.
            resultados_processados (Dict[str, Any]): Resultados consolidados das ferramentas (Etapa 5).
        """
        self.categorias_solicitadas = categorias_solicitadas
        self.resultados_processados = resultados_processados
        
    def validar(self) -> Dict[str, Any]:
        """
        Executa a validação comparando o que foi pedido com o que foi entregue.
        
        Returns:
            Dict: Objeto indicando se a validação passou ou não.
        """
        logger.info("Iniciando validação dos resultados")
        
        try:
            categorias_processadas_lista = list(self.resultados_processados.keys())
            qtd_solicitadas = len(self.categorias_solicitadas)
            qtd_processadas = len(categorias_processadas_lista)
            
            # Verificar se todas as categorias solicitadas estão presentes
            categorias_faltantes = [cat for cat in self.categorias_solicitadas if cat not in categorias_processadas_lista]
            
            if categorias_faltantes:
                logger.warning(f"Categorias faltantes: {categorias_faltantes}")
                return {
                    "validacao": False,
                    "motivo": f"As seguintes categorias solicitadas não foram processadas: {', '.join(categorias_faltantes)}",
                    "categorias_solicitadas": qtd_solicitadas,
                    "categorias_processadas": qtd_processadas
                }
                
            # Verificar se alguma ferramenta retornou erro ou estado incompleto
            for categoria, resultado in self.resultados_processados.items():
                if isinstance(resultado, dict):
                    status = resultado.get("status", "")
                    if status in ["erro", "incompleto", "dados_insuficientes"]:
                        motivo = resultado.get("motivo") or resultado.get("mensagem") or "Falha reportada pela ferramenta."
                        logger.warning(f"Falha detectada na categoria {categoria}: {status}")
                        return {
                            "validacao": False,
                            "motivo": f"A categoria '{categoria}' falhou: {motivo}",
                            "categorias_solicitadas": qtd_solicitadas,
                            "categorias_processadas": qtd_processadas
                        }
            
            # Se passou em tudo
            logger.info("Validação concluída com sucesso.")
            return {
                "validacao": True,
                "categorias_solicitadas": qtd_solicitadas,
                "categorias_processadas": qtd_processadas
            }
            
        except Exception as e:
            logger.error(f"Erro durante a etapa de validação: {str(e)}")
            return {
                "validacao": False,
                "motivo": f"Erro interno durante a validação: {str(e)}"
            }

def validar_resultados(categorias_solicitadas: List[str], resultados_processados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal para executar a validação final (Etapa 6).
    
    Args:
        categorias_solicitadas (List[str]): Categorias pedidas inicialmente pelo usuário.
        resultados_processados (Dict[str, Any]): O output consolidado (Etapa 5).
        
    Returns:
        Dict: Resultado da validação conforme definido no contrato.
    """
    validador = ValidadorRelatorio(categorias_solicitadas, resultados_processados)
    return validador.validar()

# ==============================================================================
# Exemplo de uso
# ==============================================================================
if __name__ == "__main__":
    categorias = ["estrutura", "referencias", "ortografia"]
    
    resultados_bons = {
        "estrutura": {"categoria": "estrutura", "introducao": True, "desenvolvimento": True, "conclusao": False},
        "referencias": {"categoria": "referencias", "quantidade": 8},
        "ortografia": {"categoria": "ortografia", "erros": 12}
    }
    
    print("Teste com sucesso:")
    print(validar_resultados(categorias, resultados_bons))
    
    print("\nTeste com categoria faltando:")
    resultados_faltantes = {
        "estrutura": {"categoria": "estrutura", "introducao": True}
    }
    print(validar_resultados(categorias, resultados_faltantes))
    
    print("\nTeste com ferramenta reportando erro:")
    resultados_com_erro = {
        "estrutura": {"categoria": "estrutura", "introducao": True},
        "referencias": {"categoria": "referencias", "status": "erro", "mensagem": "Falha na leitura"},
        "ortografia": {"categoria": "ortografia", "erros": 0}
    }
    print(validar_resultados(categorias, resultados_com_erro))
