"""
Módulo de Verificação de Ortografia

Este módulo verifica erros ortográficos em documentos acadêmicos.
Identifica palavras incorretas, acentuação inadequada e padrões comuns de erros.

Responsabilidades:
- Detectar palavras com possíveis erros ortográficos
- Sugerir correções
- Identificar padrões de erros comuns
- Contar total de erros encontrados
"""

import re
import logging
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VerificadorOrtografia:
    """
    Classe responsável pela verificação de ortografia em textos em português.
    
    Attributes:
        texto (str): Texto para análise
        erros_encontrados (List[Dict]): Lista de erros identificados
        quantidade_erros (int): Total de erros encontrados
    """
    
    # Dicionário de palavras comuns em português (simplificado)
    # Em produção, seria melhor usar uma biblioteca como `pyspellchecker` ou `language_tool`
    PALAVRAS_VALIDAS = {
        # Preposições
        'a', 'ante', 'após', 'até', 'com', 'contra', 'de', 'desde', 'devendo',
        'durante', 'e', 'em', 'entre', 'era', 'eram', 'essa', 'esse', 'esta',
        'estamos', 'estando', 'estar', 'estas', 'este', 'esteja', 'estejam',
        'estejamos', 'estejas', 'estemos', 'estes', 'esteve', 'estevemos',
        'estive', 'estivemos', 'estivera', 'estiverados', 'estiveram',
        'estivéramos', 'estiveras', 'estivéreis', 'estiverem', 'estivéremos',
        'estiverei', 'estiveria', 'estiveríamos', 'estiverias', 'estiveríeis',
        'estivérmos', 'estivendo', 'estiver', 'estivera', 'estivéramos',
        'estiveras', 'estivéreis', 'estiverem', 'estivéremos', 'estiverei',
        'estiveria', 'estiveríamos', 'estiverias', 'estiveríeis', 'estivérmos',
        'estive', 'estivemos', 'estive', 'estavam', 'estava', 'estávamos',
        'estáva', 'estáveis', 'está', 'estão', 'estamos', 'está', 'estão',
        'estay', 'estás', 'estái', 'estáis', 'estávamos', 'estais', 'estámos',
        # Artigos
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
        # Pronomes
        'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas', 'me', 'te',
        'se', 'nos', 'vos', 'lhe', 'lhes', 'meu', 'teu', 'seu', 'nosso',
        'vosso', 'minha', 'tinha', 'sua', 'nossa', 'vossa', 'meus', 'teus',
        'seus', 'nossos', 'vossos', 'minhas', 'tinhas', 'suas', 'nossas',
        'vossas', 'este', 'esse', 'aquele', 'esta', 'essa', 'aquela', 'isto',
        'isso', 'aquilo', 'estes', 'esses', 'aqueles', 'estas', 'essas',
        'aquelas', 'quem', 'qual', 'quanto', 'que', 'onde', 'como', 'quando',
        'porque', 'porquê',
        # Verbos comuns
        'ser', 'estar', 'ter', 'fazer', 'ir', 'vir', 'dizer', 'dar', 'poder',
        'dever', 'querer', 'saber', 'parecer', 'levar', 'deixar', 'seguir',
        'encontrar', 'chamar', 'vender', 'abrir', 'escrever', 'ler', 'conhecer',
        'trazer', 'falar', 'trabalhar', 'estudar', 'pesquisar', 'analisar',
        'demonstrar', 'verificar', 'confirmar', 'considerar', 'utilizar',
        'apresentar', 'mencionar', 'argumentar', 'concluir', 'observar',
        'realizar', 'alcançar', 'obter', 'produzir', 'compreender', 'identificar',
        # Palavras acadêmicas comuns
        'portanto', 'todavia', 'contudo', 'entretanto', 'porém', 'porém',
        'assim', 'ainda', 'também', 'semelhante', 'similar', 'próximo',
        'anterior', 'posterior', 'durante', 'através', 'conforme', 'segundo',
        'relação', 'relações', 'objetivo', 'objetivos', 'resultado', 'resultados',
        'conclusão', 'conclusões', 'introdução', 'desenvolvimento', 'referências',
        'metodologia', 'método', 'análise', 'análises', 'pesquisa', 'estudo',
        'trabalho', 'projeto', 'artigo', 'documento', 'página', 'páginas',
    }
    
    # Erros comuns e suas correções
    ERROS_COMUNS = {
        'q': 'que',
        'pq': 'porque',
        'tb': 'também',
        'tbm': 'também',
        'vc': 'você',
        'vcs': 'vocês',
        'msg': 'mensagem',
        'msgs': 'mensagens',
        'aprox': 'aproximadamente',
        'obs': 'observação',
        'etc': 'et cetera',
        'conc': 'conclusão',
        'intro': 'introdução',
        'ref': 'referência',
        'refs': 'referências',
        'n': 'não',
        'nd': 'nada',
    }
    
    # Padrões de erros comuns (regex)
    PADROES_ERROS = [
        # Duplicação de palavras
        (r'\b(\w+)\s+\1\b', 'Palavra duplicada'),
        # Espaçamento inadequado antes de pontuação
        (r'\s+([.,;:!?])', 'Espaço antes de pontuação'),
        # Acentuação inadequada (muito simplista)
        (r'\b(este|esse|aquele|que|de|para)\s+de\s+(este|esse|aquele|que|de|para)\b', 'Possível erro de preposição'),
    ]
    
    def __init__(self, texto: str):
        """
        Inicializa o verificador com o texto do documento.
        
        Args:
            texto (str): Texto completo do documento
        """
        self.texto = texto
        self.erros_encontrados: List[Dict] = []
        self.quantidade_erros = 0
        self.palavras_suspeitas: List[str] = []
        self.sugestoes: Dict[str, List[str]] = {}
        
        logger.info("Verificador de ortografia inicializado")
    
    def verificar_ortografia(self) -> Dict:
        """
        Realiza a verificação completa de ortografia do documento.
        
        Returns:
            Dict: Dicionário contendo:
                - 'categoria' (str): Sempre "ortografia"
                - 'erros' (int): Quantidade total de erros encontrados
                - 'erros_encontrados' (List[Dict]): Lista detalhada de erros
                - 'sugestoes' (Dict): Sugestões de correção
                - 'palavras_suspeitas' (List[str]): Palavras identificadas como potencial erro
                - 'mensagem' (str): Mensagem de status
        """
        try:
            logger.info("Iniciando verificação de ortografia")
            
            # Passo 1: Verificar padrões de erros comuns
            self._verificar_padroes_comuns()
            
            # Passo 2: Verificar palavras individuais
            self._verificar_palavras()
            
            # Passo 3: Contar erros
            self.quantidade_erros = len(self.erros_encontrados)
            
            logger.info(f"Verificação concluída: {self.quantidade_erros} erro(s) encontrado(s)")
            
            return {
                'categoria': 'ortografia',
                'erros': self.quantidade_erros,
                'erros_encontrados': self.erros_encontrados,
                'sugestoes': self.sugestoes,
                'palavras_suspeitas': self.palavras_suspeitas[:20],  # Limitar a 20
                'mensagem': f'{self.quantidade_erros} possível(is) erro(s) encontrado(s)' if self.quantidade_erros > 0 
                           else 'Nenhum erro ortográfico aparente'
            }
            
        except Exception as e:
            erro = f"Erro ao verificar ortografia: {str(e)}"
            logger.error(erro)
            return {
                'categoria': 'ortografia',
                'erros': 0,
                'erros_encontrados': [],
                'sugestoes': {},
                'palavras_suspeitas': [],
                'mensagem': erro,
                'erro': str(e)
            }
    
    def _verificar_padroes_comuns(self) -> None:
        """
        Verifica padrões comuns de erros usando regex.
        """
        linhas = self.texto.split('\n')
        
        for num_linha, linha in enumerate(linhas, start=1):
            for padrao, descricao in self.PADROES_ERROS:
                matches = re.finditer(padrao, linha, re.IGNORECASE)
                
                for match in matches:
                    texto_encontrado = match.group(0)
                    posicao = match.start()
                    
                    # Pular erros de espaçamento em URLs ou emails
                    if posicao > 0 and linha[posicao - 1] in ['/', '@', ':']:
                        continue
                    
                    self.erros_encontrados.append({
                        'tipo': descricao,
                        'linha': num_linha,
                        'posicao': posicao,
                        'texto': texto_encontrado,
                        'sugestao': self._gerar_sugestao(texto_encontrado, descricao)
                    })
                    
                    logger.debug(f"Padrão encontrado na linha {num_linha}: {texto_encontrado}")
    
    def _verificar_palavras(self) -> None:
        """
        Verifica palavras individuais contra dicionário e padrões.
        """
        # Extrair palavras do texto
        palavras = re.findall(r'\b[a-záàâãéèêíóôõöüçñ]+\b', self.texto.lower())
        
        for palavra in palavras:
            # Verificar contra dicionário
            if palavra not in self.PALAVRAS_VALIDAS:
                # Verificar se é um erro comum
                if palavra in self.ERROS_COMUNS:
                    self._registrar_erro_palavra(palavra, 'Erro comum', 
                                                self.ERROS_COMUNS[palavra])
                    self.palavras_suspeitas.append(palavra)
                
                # Verificar se pode ser uma palavra estrangeira ou nome próprio (muito longo ou com padrão específico)
                elif not self._eh_palavra_valida(palavra):
                    self.palavras_suspeitas.append(palavra)
        
        # Contar frequência de palavras suspeitas
        contador_palavras = Counter(self.palavras_suspeitas)
        for palavra, frequencia in contador_palavras.most_common(20):
            if frequencia >= 2:  # Só considerar palavras que aparecem mais de uma vez
                sugestoes = self._encontrar_sugestoes_similares(palavra)
                if sugestoes:
                    self.sugestoes[palavra] = sugestoes
    
    def _eh_palavra_valida(self, palavra: str) -> bool:
        """
        Verifica se uma palavra é válida mesmo que não esteja no dicionário.
        Palavras válidas incluem nomes próprios, palavras muito longas, etc.
        
        Args:
            palavra (str): Palavra para validar
            
        Returns:
            bool: True se a palavra é válida
        """
        # Palavras muito longas provavelmente são válidas (termos técnicos)
        if len(palavra) > 15:
            return True
        
        # Palavras com números ou símbolos especiais
        if any(char.isdigit() for char in palavra):
            return True
        
        # Palavras em maiúsculas (possível nome próprio)
        # Já convertemos para lowercase, então verificar no original
        if palavra[0].isupper():
            return True
        
        return False
    
    def _encontrar_sugestoes_similares(self, palavra: str, max_sugestoes: int = 3) -> List[str]:
        """
        Encontra palavras similares que podem ser correções.
        
        Args:
            palavra (str): Palavra para encontrar sugestões
            max_sugestoes (int): Número máximo de sugestões
            
        Returns:
            List[str]: Lista de sugestões similares
        """
        sugestoes = []
        
        # Usar distância de Levenshtein simplificada
        for palavra_valida in list(self.PALAVRAS_VALIDAS)[:200]:  # Limitar busca
            if self._distancia_levenshtein(palavra, palavra_valida) <= 2:
                sugestoes.append(palavra_valida)
                if len(sugestoes) >= max_sugestoes:
                    break
        
        return sugestoes
    
    def _distancia_levenshtein(self, s1: str, s2: str) -> int:
        """
        Calcula a distância de Levenshtein entre duas strings.
        
        Args:
            s1 (str): Primeira string
            s2 (str): Segunda string
            
        Returns:
            int: Distância entre as strings
        """
        if len(s1) < len(s2):
            return self._distancia_levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        linha_anterior = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            linha_atual = [i + 1]
            for j, c2 in enumerate(s2):
                # Custo de inserção, deleção, substituição
                inserirs = linha_anterior[j + 1] + 1
                deleca = linha_atual[j] + 1
                substitui = linha_anterior[j] + (c1 != c2)
                linha_atual.append(min(inserirs, deleca, substitui))
            
            linha_anterior = linha_atual
        
        return linha_anterior[-1]
    
    def _registrar_erro_palavra(self, palavra: str, tipo: str, sugestao: str) -> None:
        """
        Registra um erro de palavra encontrado.
        
        Args:
            palavra (str): Palavra com erro
            tipo (str): Tipo de erro
            sugestao (str): Sugestão de correção
        """
        # Encontrar todas as ocorrências da palavra no texto
        padrao = r'\b' + re.escape(palavra) + r'\b'
        for match in re.finditer(padrao, self.texto, re.IGNORECASE):
            linha = self.texto[:match.start()].count('\n') + 1
            posicao = match.start() - self.texto.rfind('\n', 0, match.start())
            
            self.erros_encontrados.append({
                'tipo': tipo,
                'palavra': palavra,
                'linha': linha,
                'posicao': posicao,
                'sugestao': sugestao
            })
    
    def _gerar_sugestao(self, texto_encontrado: str, tipo_erro: str) -> str:
        """
        Gera sugestão de correção baseada no tipo de erro.
        
        Args:
            texto_encontrado (str): Texto com erro
            tipo_erro (str): Tipo de erro
            
        Returns:
            str: Sugestão de correção
        """
        if 'Palavra duplicada' in tipo_erro:
            palavras = texto_encontrado.split()
            return palavras[0]
        
        elif 'Espaço antes de pontuação' in tipo_erro:
            return re.sub(r'\s+([.,;:!?])', r'\1', texto_encontrado)
        
        return texto_encontrado
    
    def obter_erros_por_linha(self) -> Dict[int, List[Dict]]:
        """
        Organiza os erros por número de linha.
        
        Returns:
            Dict: Dicionário com erros agrupados por linha
        """
        erros_por_linha = defaultdict(list)
        
        for erro in self.erros_encontrados:
            linha = erro.get('linha', 0)
            erros_por_linha[linha].append(erro)
        
        return dict(erros_por_linha)
    
    def obter_resumo_erros(self) -> Dict:
        """
        Retorna um resumo dos tipos de erros encontrados.
        
        Returns:
            Dict: Resumo com contagem por tipo de erro
        """
        resumo = defaultdict(int)
        
        for erro in self.erros_encontrados:
            tipo = erro.get('tipo', 'Desconhecido')
            resumo[tipo] += 1
        
        return dict(resumo)


def verificar_ortografia(texto: str) -> Dict:
    """
    Função auxiliar para verificar ortografia em um texto.
    
    Esta função é um wrapper simples para facilitar o uso do VerificadorOrtografia
    em contextos de chamadas de função simplificadas.
    
    Args:
        texto (str): Texto do documento para análise
        
    Returns:
        Dict: Resultado da verificação contendo:
            - categoria (str): Sempre "ortografia"
            - erros (int): Quantidade total de erros
            - erros_encontrados (List[Dict]): Detalhes dos erros
            - sugestoes (Dict): Sugestões de correção
            - mensagem (str): Mensagem de status
    """
    try:
        verificador = VerificadorOrtografia(texto)
        return verificador.verificar_ortografia()
    except Exception as e:
        logger.error(f"Erro ao verificar ortografia: {str(e)}")
        return {
            'categoria': 'ortografia',
            'erros': 0,
            'erros_encontrados': [],
            'sugestoes': {},
            'palavras_suspeitas': [],
            'mensagem': str(e),
            'erro': str(e)
        }


# ==============================================================================
# Exemplos de uso (para testes e documentação)
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("EXEMPLO: Verificação de Ortografia")
    print("="*80)
    
    # Exemplo de texto com erros
    texto_exemplo = """
    INTRODUÇÃO
    
    Este documento apresenta um estudo sobre ortografia em textos acadêmicos.
    Muitas vezes, encontramos erros que passam despercebidos.
    Pq é importante verificar o texto antes de submeter?
    Existem vários motivos q justificam essa prática.
    
    Este documento apresenta um estudo estudo sobre ortografia.
    Conforme Pereira (2020), a verificação de ortografia  é essencial.
    
    CONCLUSÃO
    
    Em conclusão, foi demonstrado q a ortografia é fundamental em textos vc acadêmicos.
    Os resultados indicam a importância dessa verificação.
    """
    
    verificador = VerificadorOrtografia(texto_exemplo)
    resultado = verificador.verificar_ortografia()
    
    print(f"\nCategoria: {resultado['categoria']}")
    print(f"Quantidade de erros: {resultado['erros']}")
    print(f"Mensagem: {resultado['mensagem']}")
    
    if resultado['erros_encontrados']:
        print("\nErros encontrados:")
        for i, erro in enumerate(resultado['erros_encontrados'][:5], 1):
            print(f"  {i}. Linha {erro.get('linha', '?')}: {erro.get('tipo', 'Desconhecido')}")
            if 'sugestao' in erro:
                print(f"     Sugestão: {erro['sugestao']}")
    
    if resultado['sugestoes']:
        print("\nSugestões:")
        for palavra, sugestoes in list(resultado['sugestoes'].items())[:5]:
            print(f"  '{palavra}' → {', '.join(sugestoes)}")
