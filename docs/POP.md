# Procedimento Operacional Padrão (POP)

## Projeto

**Agente Auditor de Documentos Configurável**

---

# 1. Objetivo

Padronizar o processo de análise preliminar de documentos acadêmicos por meio de um workflow agêntico capaz de verificar critérios selecionados pelo usuário, reduzindo o tempo gasto em tarefas repetitivas e produzindo relatórios estruturados.

---

# 2. Contexto Operacional

No ambiente acadêmico, professores, orientadores e avaliadores frequentemente recebem documentos para análise, como trabalhos, relatórios, artigos e projetos.

Antes da avaliação do conteúdo, é necessário realizar verificações iniciais, como:

* Presença de seções obrigatórias;
* Existência de referências bibliográficas;
* Identificação de erros ortográficos;
* Conferência de elementos estruturais.

Essas verificações costumam ser realizadas manualmente e demandam tempo considerável.

---

# 3. Problema

O processo de análise preliminar de documentos é repetitivo, sujeito a erros humanos e consome tempo que poderia ser utilizado em avaliações mais aprofundadas.

A ausência de uma ferramenta automatizada dificulta a padronização das verificações e aumenta o esforço necessário para revisar documentos.

---

# 4. Escopo

## Funcionalidades incluídas

* Upload de documentos PDF;
* Extração automática de texto;
* Seleção de categorias de análise;
* Verificação de estrutura do documento;
* Verificação de referências bibliográficas;
* Verificação ortográfica básica;
* Geração de relatório estruturado;
* Validação dos resultados produzidos.

## Funcionalidades fora do escopo

* Detecção de plágio;
* Correção automática do documento;
* Avaliação da qualidade científica;
* Integração com sistemas acadêmicos;
* Verificação completa das normas ABNT;
* Processamento de arquivos que não sejam PDF.

---

# 5. Entradas

O sistema recebe:

* Arquivo PDF;
* Categorias de análise selecionadas pelo usuário.

Exemplo:

```json
{
  "arquivo": "trabalho.pdf",
  "categorias": [
    "estrutura",
    "referencias",
    "ortografia"
  ]
}
```

---

# 6. Processo Atual (Manual)

1. O usuário finaliza o documento.
2. O documento é enviado para análise.
3. O avaliador abre o arquivo.
4. O avaliador verifica a estrutura.
5. O avaliador verifica referências.
6. O avaliador procura erros ortográficos.
7. O avaliador registra observações.
8. O avaliador produz um parecer inicial.

---

# 7. Processo Proposto (Automatizado)

1. O usuário envia o documento.
2. O usuário seleciona os critérios desejados.
3. O sistema extrai o texto do PDF.
4. O agente identifica quais verificações devem ser realizadas.
5. O agente executa as ferramentas necessárias.
6. Os resultados são consolidados.
7. O sistema valida os resultados.
8. Um relatório é gerado para o usuário.

---

# 8. Saída Esperada

Relatório contendo:

* Resultado da análise estrutural;
* Resultado da análise de referências;
* Resultado da análise ortográfica;
* Status geral do documento.

Exemplo:

```json
{
  "estrutura": {
    "introducao": true,
    "desenvolvimento": true,
    "conclusao": false
  },
  "referencias": {
    "quantidade": 8
  },
  "ortografia": {
    "erros": 12
  },
  "status_final": "necessita_revisao"
}
```

---

# 9. Critérios de Aceitação

O processo será considerado válido quando:

* O documento for recebido corretamente;
* O texto for extraído sem falhas;
* Todas as categorias solicitadas forem processadas;
* O relatório final for gerado;
* Os resultados forem apresentados em formato estruturado.

---

# 10. Checklist de Validação

* [x] O grupo definiu um contexto operacional conhecido.
* [x] O contexto pode ser explicado como uma rotina, processo ou POP.
* [x] O problema está descrito de forma específica.
* [x] O recorte é pequeno o suficiente para ser executado no prazo.
