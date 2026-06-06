"""
Módulo de Verificação de Estrutura de Documentos

Este módulo valida a presença dos elementos estruturais básicos de um documento acadêmico.

Responsabilidades:
- Verificar presença de Introdução
- Verificar presença de Desenvolvimento (ou seções equivalentes)
- Verificar presença de Conclusão (ou considerações finais)
"""

import re
import logging
from typing import Dict

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VerificadorEstrutura:
    """
    Classe responsável pela verificação da estrutura do documento.
    """
    
    PALAVRAS_CHAVE_INTRODUCAO = [
        r'\bintrodução\b',
        r'\bintroducao\b',
        r'\bintroduction\b'
    ]
    
    PALAVRAS_CHAVE_DESENVOLVIMENTO = [
        r'\bdesenvolvimento\b',
        r'\breferencial teórico\b',
        r'\bfundamentação teórica\b',
        r'\bmetodologia\b',
        r'\bresultados\b',
        r'\bdiscussão\b'
    ]
    
    PALAVRAS_CHAVE_CONCLUSAO = [
        r'\bconclusão\b',
        r'\bconclusao\b',
        r'\bconsiderações finais\b',
        r'\bconsideracoes finais\b',
        r'\bconclusion\b'
    ]
    
    def __init__(self, texto: str):
        self.texto = texto
        
    def verificar(self) -> Dict:
        """
        Executa a verificação estrutural.
        
        Returns:
            Dict: Resultado da verificação
        """
        try:
            if not self.texto or len(self.texto.strip()) < 100:
                logger.error("Texto insuficiente para análise da estrutura")
                return {
                    "status": "erro",
                    "codigo": "TEXTO_INSUFICIENTE"
                }
            
            texto_lower = self.texto.lower()
            
            introducao = self._verificar_secao(texto_lower, self.PALAVRAS_CHAVE_INTRODUCAO)
            desenvolvimento = self._verificar_secao(texto_lower, self.PALAVRAS_CHAVE_DESENVOLVIMENTO)
            conclusao = self._verificar_secao(texto_lower, self.PALAVRAS_CHAVE_CONCLUSAO)
            
            return {
                "categoria": "estrutura",
                "introducao": introducao,
                "desenvolvimento": desenvolvimento,
                "conclusao": conclusao
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar estrutura: {str(e)}")
            return {
                "categoria": "estrutura",
                "status": "erro",
                "codigo": "FALHA_ANALISE",
                "mensagem": str(e)
            }
            
    def _verificar_secao(self, texto: str, padroes: list) -> bool:
        """Verifica se algum dos padrões existe no texto."""
        for padrao in padroes:
            if re.search(padrao, texto, re.IGNORECASE | re.MULTILINE):
                return True
        return False

def verificar_estrutura(texto: str) -> Dict:
    """
    Função principal para verificar a estrutura do documento.
    
    Args:
        texto (str): O texto extraído do documento.
        
    Returns:
        Dict: Dicionário com os resultados da verificação estrutural conforme o contrato.
    """
    verificador = VerificadorEstrutura(texto)
    return verificador.verificar()

# ==============================================================================
# Exemplo de uso
# ==============================================================================
if __name__ == "__main__":
    texto_exemplo = '''
    Título do Trabalho
    
    1. Introdução
    Neste trabalho abordaremos a importância da tecnologia.
    
    2. Metodologia
    A pesquisa foi realizada através de revisão de literatura.
    
    3. Conclusão
    Conclui-se que a tecnologia é fundamental.
    '''
    
    resultado = verificar_estrutura(texto_exemplo)
    print("Resultado da verificação:")
    print(resultado)
