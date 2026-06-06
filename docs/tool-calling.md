# Tool Calling

## Projeto

**Agente Auditor de Documentos Configurável**

---

# Objetivo

Definir as ferramentas utilizadas pelo agente, seus parâmetros, retornos esperados e estratégias de tratamento de falhas.

O agente não executa diretamente todas as tarefas. Ele utiliza ferramentas especializadas para realizar verificações específicas dentro do workflow.

---

# Visão Geral

Durante a execução do workflow, o agente poderá chamar as seguintes ferramentas:

1. extrair_texto_pdf
2. verificar_estrutura
3. verificar_referencias
4. verificar_ortografia

Cada ferramenta possui responsabilidade única e bem definida.

---

# Ferramenta: extrair_texto_pdf

## Finalidade

Extrair o conteúdo textual de um documento PDF enviado pelo usuário.

## Quando é utilizada

Após a validação da entrada.

## Parâmetros

```json id="1nd4vw"
{
  "arquivo": "trabalho.pdf"
}
```

## Retorno Esperado

```json id="y2t7j0"
{
  "status": "sucesso",
  "texto_extraido": "conteúdo do documento",
  "paginas": 12
}
```

## Possíveis Falhas

Arquivo inválido:

```json id="hjebk8"
{
  "status": "erro",
  "codigo": "PDF_INVALIDO"
}
```

## Ação do Agente

* Registrar erro.
* Encerrar processamento.
* Solicitar novo arquivo ao usuário.

---

# Ferramenta: verificar_estrutura

## Finalidade

Verificar a presença dos elementos estruturais básicos do documento.

## Quando é utilizada

Quando a categoria "estrutura" for selecionada.

## Parâmetros

```json id="1avq5m"
{
  "texto": "conteúdo extraído"
}
```

## Retorno Esperado

```json id="pwv4lv"
{
  "categoria": "estrutura",
  "introducao": true,
  "desenvolvimento": true,
  "conclusao": false
}
```

## Possíveis Falhas

```json id="pd2ht5"
{
  "status": "erro",
  "codigo": "TEXTO_INSUFICIENTE"
}
```

## Ação do Agente

* Registrar falha.
* Marcar categoria como não concluída.
* Encaminhar para revisão humana.

---

# Ferramenta: verificar_referencias

## Finalidade

Identificar a existência de referências bibliográficas e contabilizar ocorrências.

## Quando é utilizada

Quando a categoria "referencias" for selecionada.

## Parâmetros

```json id="d2h1rn"
{
  "texto": "conteúdo extraído"
}
```

## Retorno Esperado

```json id="8jttf0"
{
  "categoria": "referencias",
  "quantidade": 8,
  "possui_secao": true
}
```

## Caso Nenhuma Referência Seja Encontrada

```json id="q91x4w"
{
  "categoria": "referencias",
  "quantidade": 0,
  "possui_secao": false
}
```

## Ação do Agente

* Registrar ocorrência.
* Incluir observação no relatório.
* Não inventar referências inexistentes.

---

# Ferramenta: verificar_ortografia

## Finalidade

Identificar possíveis erros ortográficos no texto.

## Quando é utilizada

Quando a categoria "ortografia" for selecionada.

## Parâmetros

```json id="g6lhm8"
{
  "texto": "conteúdo extraído"
}
```

## Retorno Esperado

```json id="1b0yq9"
{
  "categoria": "ortografia",
  "erros": 12
}
```

## Possíveis Falhas

```json id="vf8ymv"
{
  "status": "erro",
  "codigo": "FALHA_ANALISE"
}
```

## Ação do Agente

* Registrar erro.
* Informar falha no relatório.
* Solicitar revisão manual.

---

# Processo de Seleção de Ferramentas

O agente decide quais ferramentas executar com base nas categorias selecionadas pelo usuário.

Exemplo:

Entrada:

```json id="iqijjw"
{
  "categorias": [
    "estrutura",
    "ortografia"
  ]
}
```

Plano de execução:

```json id="frbfqg"
{
  "acoes": [
    "verificar_estrutura",
    "verificar_ortografia"
  ]
}
```

A ferramenta de referências não será executada.

---

# Tratamento de Falhas

Quando uma ferramenta falhar:

1. O erro será registrado.
2. O agente não inventará resultados.
3. A categoria será marcada como incompleta.
4. O relatório indicará necessidade de revisão humana.

Exemplo:

```json id="5ixj92"
{
  "categoria": "estrutura",
  "status": "incompleto",
  "motivo": "Falha na análise"
}
```

---

# Política para Ausência de Dados

Quando uma ferramenta não encontrar informações suficientes:

* O agente deverá informar explicitamente a ausência de dados.
* Nenhum valor será estimado ou inventado.
* O relatório indicará a limitação encontrada.

Exemplo:

```json id="0ay0yy"
{
  "status": "dados_insuficientes",
  "categoria": "referencias"
}
```

---

# Benefícios do Tool Calling

* Separação de responsabilidades.
* Maior confiabilidade do sistema.
* Facilidade de manutenção.
* Tratamento estruturado de erros.
* Possibilidade de adicionar novas ferramentas futuramente.

---

# Checklist de Validação

* [x] O grupo identificou as ferramentas necessárias.
* [x] Cada ferramenta possui finalidade clara.
* [x] Os parâmetros estão definidos.
* [x] O retorno esperado está descrito.
* [x] Existe tratamento para falhas e ausência de dados.