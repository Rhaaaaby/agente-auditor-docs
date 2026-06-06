"""
Módulo de Extração de Texto de PDFs

Este módulo é responsável pela Etapa 2 do workflow: Extração de Texto.
Realiza a leitura de arquivos PDF e extrai todo o conteúdo textual.

Responsabilidades:
- Validar existência e formato do arquivo PDF
- Extrair texto de todas as páginas
- Consolidar conteúdo de forma estruturada
- Tratar erros de leitura e acesso a arquivos
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pdfplumber


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ExtractorPDF:
    """
    Classe responsável pela extração de texto de arquivos PDF.
    
    Attributes:
        caminho_arquivo (Path): Caminho para o arquivo PDF
        text_por_pagina (List[str]): Lista com texto extraído de cada página
        texto_consolidado (str): Texto de todas as páginas concatenado
    """
    
    def __init__(self, caminho_arquivo: str):
        """
        Inicializa o extrator com o caminho do arquivo PDF.
        
        Args:
            caminho_arquivo (str): Caminho absoluto ou relativo para o arquivo PDF
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não for um PDF válido
        """
        self.caminho_arquivo = Path(caminho_arquivo)
        self.text_por_pagina: List[str] = []
        self.texto_consolidado: str = ""
        self.metadados: Dict = {}
        self.num_paginas: int = 0
        
        self._validar_arquivo()
        logger.info(f"Extrator inicializado para: {self.caminho_arquivo}")
    
    def _validar_arquivo(self) -> None:
        """
        Valida se o arquivo existe e possui extensão PDF.
        
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo não for um PDF
        """
        if not self.caminho_arquivo.exists():
            erro = f"Arquivo não encontrado: {self.caminho_arquivo}"
            logger.error(erro)
            raise FileNotFoundError(erro)
        
        if self.caminho_arquivo.suffix.lower() != '.pdf':
            erro = f"Arquivo não é um PDF válido: {self.caminho_arquivo.suffix}"
            logger.error(erro)
            raise ValueError(erro)
        
        logger.info(f"Validação concluída: {self.caminho_arquivo}")
    
    def extrair_texto(self) -> Dict:
        """
        Extrai texto de todas as páginas do PDF.
        
        Returns:
            Dict: Dicionário contendo:
                - 'sucesso' (bool): Se a extração foi bem-sucedida
                - 'texto_extraido' (str): Texto consolidado de todas as páginas
                - 'num_paginas' (int): Quantidade de páginas processadas
                - 'texto_por_pagina' (List[str]): Texto de cada página
                - 'metadados' (Dict): Informações sobre o PDF
                - 'tamanho_arquivo' (int): Tamanho em bytes
                - 'mensagem' (str): Mensagem de status
                
        Raises:
            Exception: Se ocorrer erro durante a leitura do PDF
        """
        try:
            logger.info(f"Iniciando extração de texto: {self.caminho_arquivo}")
            
            with pdfplumber.open(self.caminho_arquivo) as pdf:
                # Extrair metadados
                self.metadados = pdf.metadata or {}
                self.num_paginas = len(pdf.pages)
                
                logger.info(f"PDF contém {self.num_paginas} página(s)")
                
                # Extrair texto de cada página
                for idx, pagina in enumerate(pdf.pages, start=1):
                    try:
                        texto_pagina = pagina.extract_text() or ""
                        self.text_por_pagina.append(texto_pagina)
                        logger.debug(f"Página {idx} extraída: {len(texto_pagina)} caracteres")
                    except Exception as e:
                        erro_msg = f"Erro ao extrair texto da página {idx}: {str(e)}"
                        logger.warning(erro_msg)
                        self.text_por_pagina.append(f"[ERRO NA PÁGINA {idx}]")
                
                # Consolidar texto
                self._consolidar_texto()
            
            # Preparar resultado
            tamanho_arquivo = self.caminho_arquivo.stat().st_size
            resultado = {
                'sucesso': True,
                'texto_extraido': self.texto_consolidado,
                'num_paginas': self.num_paginas,
                'texto_por_pagina': self.text_por_pagina,
                'metadados': self.metadados,
                'tamanho_arquivo': tamanho_arquivo,
                'mensagem': f'Texto extraído com sucesso de {self.num_paginas} página(s)'
            }
            
            logger.info(f"Extração concluída: {len(self.texto_consolidado)} caracteres")
            return resultado
            
        except pdfplumber.PDFException as e:
            erro = f"Erro ao abrir PDF: {str(e)}"
            logger.error(erro)
            return {
                'sucesso': False,
                'texto_extraido': "",
                'num_paginas': 0,
                'texto_por_pagina': [],
                'metadados': {},
                'tamanho_arquivo': 0,
                'mensagem': erro,
                'erro': str(e)
            }
        except Exception as e:
            erro = f"Erro inesperado na extração: {str(e)}"
            logger.error(erro)
            return {
                'sucesso': False,
                'texto_extraido': "",
                'num_paginas': 0,
                'texto_por_pagina': [],
                'metadados': {},
                'tamanho_arquivo': 0,
                'mensagem': erro,
                'erro': str(e)
            }
    
    def _consolidar_texto(self) -> None:
        """
        Consolida o texto de todas as páginas em um único texto.
        Adiciona separadores entre as páginas para melhor organização.
        """
        separador = "\n" + "="*80 + "\n"
        self.texto_consolidado = separador.join(self.text_por_pagina)
        logger.debug(f"Texto consolidado: {len(self.texto_consolidado)} caracteres")
    
    def extrair_texto_por_pagina(self, numero_pagina: int) -> Optional[str]:
        """
        Retorna o texto de uma página específica.
        
        Args:
            numero_pagina (int): Número da página (começando em 1)
            
        Returns:
            Optional[str]: Texto da página ou None se não existir
        """
        if 1 <= numero_pagina <= len(self.text_por_pagina):
            return self.text_por_pagina[numero_pagina - 1]
        else:
            logger.warning(f"Página {numero_pagina} não encontrada")
            return None
    
    def obter_metadados(self) -> Dict:
        """
        Retorna os metadados do PDF.
        
        Returns:
            Dict: Dicionário com metadados do PDF (autor, título, data, etc.)
        """
        return self.metadados
    
    def obter_numero_paginas(self) -> int:
        """
        Retorna a quantidade total de páginas do PDF.
        
        Returns:
            int: Número de páginas
        """
        return self.num_paginas


def extrair_pdf(caminho_arquivo: str) -> Dict:
    """
    Função auxiliar para extrair texto de um PDF.
    
    Esta função é um wrapper simples para facilitar o uso do ExtractorPDF
    em contextos de chamadas de função simplificadas.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo PDF
        
    Returns:
        Dict: Resultado da extração contendo:
            - sucesso (bool)
            - texto_extraido (str)
            - num_paginas (int)
            - mensagem (str)
            - E outros campos de suporte
    """
    try:
        extrator = ExtractorPDF(caminho_arquivo)
        return extrator.extrair_texto()
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Erro de validação: {str(e)}")
        return {
            'sucesso': False,
            'texto_extraido': "",
            'num_paginas': 0,
            'texto_por_pagina': [],
            'metadados': {},
            'tamanho_arquivo': 0,
            'mensagem': str(e),
            'erro': str(e)
        }


# ==============================================================================
# Exemplos de uso (para testes e documentação)
# ==============================================================================

if __name__ == "__main__":
    # Exemplo 1: Extração simples
    print("\n" + "="*80)
    print("EXEMPLO 1: Extração Simples")
    print("="*80)
    
    # Descomente e forneça um caminho real para testar
    # resultado = extrair_pdf("caminho/para/seu/documento.pdf")
    # print(f"Sucesso: {resultado['sucesso']}")
    # print(f"Páginas: {resultado['num_paginas']}")
    # print(f"Caracteres: {len(resultado['texto_extraido'])}")
    # print(f"Mensagem: {resultado['mensagem']}")
    
    print("\nPara usar, forneça o caminho de um PDF real:")
    print("  resultado = extrair_pdf('documento.pdf')")
    print("  if resultado['sucesso']:")
    print("      print(resultado['texto_extraido'])")
    
    # Exemplo 2: Usando a classe diretamente
    print("\n" + "="*80)
    print("EXEMPLO 2: Usando a Classe ExtractorPDF")
    print("="*80)
    
    print("\n  extrator = ExtractorPDF('documento.pdf')")
    print("  resultado = extrator.extrair_texto()")
    print("  texto_pagina_1 = extrator.extrair_texto_por_pagina(1)")
    print("  metadados = extrator.obter_metadados()")
