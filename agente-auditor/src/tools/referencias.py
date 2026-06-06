"""
Módulo de Validação de Referências Bibliográficas

Este módulo valida as referências bibliográficas de um documento acadêmico.
Detecta e valida diferentes formatos de citações (ABNT, APA, Harvard, etc.)

Responsabilidades:
- Detectar seção de referências no texto
- Identificar e contar referências
- Validar formato de referências
- Verificar padrões de citação
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FormatoReferencia(Enum):
    """Formatos de referência suportados."""
    ABNT = "ABNT"
    APA = "APA"
    HARVARD = "Harvard"
    VANCOUVER = "Vancouver"
    CHICAGO = "Chicago"
    DESCONHECIDO = "Desconhecido"


class ValidadorReferencias:
    """
    Classe responsável pela validação de referências bibliográficas.
    
    Attributes:
        texto (str): Texto do documento para análise
        referencias_encontradas (List[str]): Lista de referências identificadas
        quantidade (int): Total de referências encontradas
        formatos_detectados (List[FormatoReferencia]): Formatos de referência detectados
    """
    
    # Padrões regex para diferentes formatos
    PADROES_ABNT = [
        # ABNT básico: AUTOR. Título. Editora, ano.
        r'^[A-Z][A-Za-z\s,\.]*\.\s+[A-Z][^\.]*\.\s+[^,]+,\s+\d{4}\.',
        # Com et al.
        r'^[A-Z][A-Za-z\s,\.]*\s+et\s+al\.\s+[A-Z][^\.]*\.\s+[^,]+,\s+\d{4}\.',
    ]
    
    PADROES_APA = [
        # APA: Autor, A. A. (Ano). Título.
        r'^[A-Z][a-z]+,\s+[A-Z]\..*\(\d{4}\)\.',
        # Com et al.
        r'^[A-Z][a-z]+,\s+[A-Z]\.\s+et\s+al\.\s*\(\d{4}\)\.',
    ]
    
    PADROES_HARVARD = [
        # Harvard: Author, A., Year. Title.
        r'^[A-Z][a-z]+,\s+[A-Z]\.,\s+\d{4}\.',
        # Com et al.
        r'^[A-Z][a-z]+\s+et\s+al\.,\s+\d{4}\.',
    ]
    
    PADROES_VANCOUVER = [
        # Vancouver: [1] Author AA, Author BB. Title.
        r'^\[\d+\]\s+[A-Z][a-z]+\s+[A-Z]{2}.*\.',
    ]
    
    # Palavras-chave para seção de referências
    PALAVRAS_CHAVE_SECAO = [
        r'\breferências\b',
        r'\breferences\b',
        r'\bbibliografia\b',
        r'\bbibliography\b',
        r'\bworks\s+cited\b',
        r'\bobras\s+citadas\b',
    ]
    
    # Padrão genérico para referências
    PADRAO_GENERICO = r'^(?:[A-Z][\w\s,\.;:\'"\-\(\)]+){10,}$'
    
    def __init__(self, texto: str):
        """
        Inicializa o validador com o texto do documento.
        
        Args:
            texto (str): Texto completo do documento
        """
        self.texto = texto
        self.referencias_encontradas: List[str] = []
        self.quantidade = 0
        self.formatos_detectados: List[FormatoReferencia] = []
        self.secao_referencias: str = ""
        self.linhas_referencias: List[str] = []
        
        logger.info("Validador de referências inicializado")
    
    def validar_referencias(self) -> Dict:
        """
        Valida as referências bibliográficas do documento.
        
        Returns:
            Dict: Dicionário contendo:
                - 'categoria' (str): Sempre "referencias"
                - 'quantidade' (int): Total de referências encontradas
                - 'existe' (bool): Se há referências no documento
                - 'formatos_detectados' (List[str]): Formatos identificados
                - 'referencias' (List[str]): Lista de referências encontradas
                - 'secao_completa' (str): Texto completo da seção de referências
                - 'mensagem' (str): Mensagem de status
        """
        try:
            logger.info("Iniciando validação de referências")
            
            # Passo 1: Identificar seção de referências
            self._extrair_secao_referencias()
            
            if not self.secao_referencias:
                logger.warning("Nenhuma seção de referências encontrada")
                return {
                    'categoria': 'referencias',
                    'quantidade': 0,
                    'existe': False,
                    'formatos_detectados': [],
                    'referencias': [],
                    'secao_completa': "",
                    'mensagem': 'Nenhuma seção de referências encontrada no documento'
                }
            
            # Passo 2: Extrair linhas de referências
            self._extrair_linhas_referencias()
            
            # Passo 3: Detectar formatos
            self._detectar_formatos()
            
            # Passo 4: Contar referências
            self.quantidade = len(self.referencias_encontradas)
            
            logger.info(f"Validação concluída: {self.quantidade} referências encontradas")
            
            return {
                'categoria': 'referencias',
                'quantidade': self.quantidade,
                'existe': self.quantidade > 0,
                'formatos_detectados': [fmt.value for fmt in self.formatos_detectados],
                'referencias': self.referencias_encontradas,
                'secao_completa': self.secao_referencias,
                'mensagem': f'{self.quantidade} referência(s) encontrada(s)' if self.quantidade > 0 
                           else 'Nenhuma referência encontrada'
            }
            
        except Exception as e:
            erro = f"Erro ao validar referências: {str(e)}"
            logger.error(erro)
            return {
                'categoria': 'referencias',
                'quantidade': 0,
                'existe': False,
                'formatos_detectados': [],
                'referencias': [],
                'secao_completa': "",
                'mensagem': erro,
                'erro': str(e)
            }
    
    def _extrair_secao_referencias(self) -> None:
        """
        Extrai a seção de referências do texto.
        Procura por palavras-chave e captura tudo após elas.
        """
        texto_lower = self.texto.lower()
        
        # Procurar por palavras-chave
        for palavra_chave in self.PALAVRAS_CHAVE_SECAO:
            match = re.search(palavra_chave, texto_lower, re.IGNORECASE | re.MULTILINE)
            if match:
                inicio = match.start()
                # Capturar desde a palavra-chave até o final do texto
                self.secao_referencias = self.texto[inicio:]
                logger.debug(f"Seção de referências encontrada com padrão: {palavra_chave}")
                return
        
        # Se não encontrou por palavras-chave, tenta procurar por padrão de referências
        # nas últimas 30% do documento
        tamanho = len(self.texto)
        inicio_busca = int(tamanho * 0.7)
        
        linhas = self.texto[inicio_busca:].split('\n')
        for idx, linha in enumerate(linhas):
            if self._eh_referencia(linha):
                # Encontrou primeira referência, extrai daqui em diante
                self.secao_referencias = '\n'.join(linhas[idx:])
                logger.debug("Seção de referências identificada por padrão de referência")
                return
    
    def _extrair_linhas_referencias(self) -> None:
        """
        Extrai cada linha individual de referência da seção.
        """
        if not self.secao_referencias:
            return
        
        linhas = self.secao_referencias.split('\n')
        
        for linha in linhas:
            linha_limpa = linha.strip()
            
            # Ignorar linhas vazias, títulos e muito curtas
            if not linha_limpa or len(linha_limpa) < 10:
                continue
            
            # Verificar se é uma referência
            if self._eh_referencia(linha_limpa):
                self.referencias_encontradas.append(linha_limpa)
                logger.debug(f"Referência extraída: {linha_limpa[:50]}...")
    
    def _eh_referencia(self, linha: str) -> bool:
        """
        Verifica se uma linha é uma referência válida.
        
        Args:
            linha (str): Linha de texto para verificar
            
        Returns:
            bool: True se é uma referência, False caso contrário
        """
        linha_limpa = linha.strip()
        
        if len(linha_limpa) < 10:
            return False
        
        # Verificar padrões específicos
        for padroes in [self.PADROES_ABNT, self.PADROES_APA, self.PADROES_HARVARD, self.PADROES_VANCOUVER]:
            for padrao in padroes:
                if re.match(padrao, linha_limpa, re.IGNORECASE):
                    return True
        
        # Verificar padrão genérico
        # Deve ter números (ano provável), maiúsculas, pontuação
        tem_ano = re.search(r'\d{4}', linha_limpa)
        tem_maiuscula = re.search(r'[A-Z]', linha_limpa)
        tem_pontuacao = any(char in linha_limpa for char in '.,:;')
        
        if tem_ano and tem_maiuscula and tem_pontuacao:
            return True
        
        return False
    
    def _detectar_formatos(self) -> None:
        """
        Detecta os formatos de referência utilizados no documento.
        """
        formatos = set()
        
        for ref in self.referencias_encontradas:
            # Verificar ABNT
            if any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_ABNT):
                formatos.add(FormatoReferencia.ABNT)
            
            # Verificar APA
            elif any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_APA):
                formatos.add(FormatoReferencia.APA)
            
            # Verificar Harvard
            elif any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_HARVARD):
                formatos.add(FormatoReferencia.HARVARD)
            
            # Verificar Vancouver
            elif any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_VANCOUVER):
                formatos.add(FormatoReferencia.VANCOUVER)
        
        self.formatos_detectados = list(formatos) if formatos else [FormatoReferencia.DESCONHECIDO]
        logger.info(f"Formatos detectados: {[f.value for f in self.formatos_detectados]}")
    
    def obter_referencias_por_formato(self, formato: FormatoReferencia) -> List[str]:
        """
        Retorna apenas as referências de um formato específico.
        
        Args:
            formato (FormatoReferencia): Formato desejado
            
        Returns:
            List[str]: Lista de referências do formato especificado
        """
        referencias_filtradas = []
        
        for ref in self.referencias_encontradas:
            if formato == FormatoReferencia.ABNT:
                if any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_ABNT):
                    referencias_filtradas.append(ref)
            
            elif formato == FormatoReferencia.APA:
                if any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_APA):
                    referencias_filtradas.append(ref)
            
            elif formato == FormatoReferencia.HARVARD:
                if any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_HARVARD):
                    referencias_filtradas.append(ref)
            
            elif formato == FormatoReferencia.VANCOUVER:
                if any(re.match(p, ref, re.IGNORECASE) for p in self.PADROES_VANCOUVER):
                    referencias_filtradas.append(ref)
        
        return referencias_filtradas
    
    def validar_consistencia(self) -> Dict:
        """
        Valida se as referências estão em formato consistente.
        
        Returns:
            Dict: Informações sobre consistência
        """
        if not self.referencias_encontradas:
            return {
                'consistente': False,
                'motivo': 'Nenhuma referência encontrada'
            }
        
        # Se tem apenas 1 formato, é consistente
        if len(self.formatos_detectados) == 1:
            return {
                'consistente': True,
                'formato': self.formatos_detectados[0].value,
                'motivo': 'Todas as referências usam o mesmo formato'
            }
        
        return {
            'consistente': False,
            'motivo': f'Múltiplos formatos detectados: {[f.value for f in self.formatos_detectados]}'
        }


def validar_referencias(texto: str) -> Dict:
    """
    Função auxiliar para validar referências em um texto.
    
    Esta função é um wrapper simples para facilitar o uso do ValidadorReferencias
    em contextos de chamadas de função simplificadas.
    
    Args:
        texto (str): Texto do documento para análise
        
    Returns:
        Dict: Resultado da validação contendo:
            - categoria (str): Sempre "referencias"
            - quantidade (int): Total de referências
            - existe (bool): Se há referências
            - formatos_detectados (List[str]): Formatos identificados
            - referencias (List[str]): Lista de referências
            - mensagem (str): Mensagem de status
    """
    try:
        validador = ValidadorReferencias(texto)
        return validador.validar_referencias()
    except Exception as e:
        logger.error(f"Erro ao validar referências: {str(e)}")
        return {
            'categoria': 'referencias',
            'quantidade': 0,
            'existe': False,
            'formatos_detectados': [],
            'referencias': [],
            'secao_completa': "",
            'mensagem': str(e),
            'erro': str(e)
        }


# ==============================================================================
# Exemplos de uso (para testes e documentação)
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("EXEMPLO: Validação de Referências")
    print("="*80)
    
    # Exemplo de texto com referências
    texto_exemplo = """
    INTRODUÇÃO
    Este é um documento de exemplo com referências.
    
    DESENVOLVIMENTO
    Conforme Silva et al. (2020) demonstram...
    
    REFERÊNCIAS
    
    Silva, J. A., Santos, M. B., & Oliveira, C. D. (2020). Título do artigo.
    Revista Científica, 15(3), 45-67.
    
    Costa, P. R. (2019). Um estudo sobre tecnologia. Editora Universitária, 2019.
    
    Pereira, A. B., et al. (2021). Referências em documentos acadêmicos.
    Journal of Academic Studies, 8(2), 123-145.
    """
    
    validador = ValidadorReferencias(texto_exemplo)
    resultado = validador.validar_referencias()
    
    print(f"\nCategoria: {resultado['categoria']}")
    print(f"Quantidade encontrada: {resultado['quantidade']}")
    print(f"Existe: {resultado['existe']}")
    print(f"Formatos detectados: {resultado['formatos_detectados']}")
    print(f"Mensagem: {resultado['mensagem']}")
    
    if resultado['referencias']:
        print("\nReferências encontradas:")
        for i, ref in enumerate(resultado['referencias'], 1):
            print(f"  {i}. {ref[:80]}...")
