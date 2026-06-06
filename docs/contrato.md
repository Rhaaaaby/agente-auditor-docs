# Contratos de Dados

## Projeto

**Agente Auditor de Documentos Configurável**

---

# Objetivo

Definir os formatos padronizados de entrada e saída utilizados pelo workflow, garantindo consistência entre as etapas, tratamento de erros e limites claros para atuação da IA.

---

# Contrato de Entrada

Todo documento enviado ao sistema deve seguir a seguinte estrutura:

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

## Campos

| Campo      | Tipo   | Obrigatório | Descrição                            |
| ---------- | ------ | ----------- | ------------------------------------ |
| arquivo    | string | Sim         | Nome ou identificador do arquivo PDF |
| categorias | array  | Sim         | Lista de verificações solicitadas    |

## Categorias Permitidas

```json
[
  "estrutura",
  "referencias",
  "ortografia"
]
```

## Regras de Validação

* O arquivo deve existir.
* O arquivo deve estar no formato PDF.
* Deve existir pelo menos uma categoria.
* Categorias não reconhecidas serão rejeitadas.

---

# Contrato da Etapa de Extração

## Entrada

```json
{
  "arquivo": "trabalho.pdf"
}
```

## Saída

```json
{
  "texto_extraido": "conteúdo do documento",
  "paginas": 12,
  "status": "sucesso"
}
```

## Possíveis Erros

```json
{
  "status": "erro",
  "codigo": "PDF_INVALIDO",
  "mensagem": "Não foi possível extrair o texto."
}
```

---

# Contrato da Ferramenta verificar_estrutura

## Entrada

```json
{
  "texto": "conteúdo extraído"
}
```

## Saída

```json
{
  "categoria": "estrutura",
  "introducao": true,
  "desenvolvimento": true,
  "conclusao": false
}
```

## Resposta Incompleta

```json
{
  "categoria": "estrutura",
  "status": "incompleto",
  "motivo": "Texto insuficiente para análise."
}
```

---

# Contrato da Ferramenta verificar_referencias

## Entrada

```json
{
  "texto": "conteúdo extraído"
}
```

## Saída

```json
{
  "categoria": "referencias",
  "quantidade": 8,
  "possui_secao": true
}
```

## Ausência de Dados

```json
{
  "categoria": "referencias",
  "quantidade": 0,
  "possui_secao": false
}
```

---

# Contrato da Ferramenta verificar_ortografia

## Entrada

```json
{
  "texto": "conteúdo extraído"
}
```

## Saída

```json
{
  "categoria": "ortografia",
  "erros": 12
}
```

## Erro de Processamento

```json
{
  "categoria": "ortografia",
  "status": "erro",
  "mensagem": "Falha durante análise ortográfica."
}
```

---

# Contrato de Consolidação

## Entrada

Resultados produzidos pelas ferramentas executadas.

## Saída

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
  }
}
```

---

# Contrato da Saída Final

A resposta final do sistema deverá seguir o formato:

```json
{
  "status_final": "necessita_revisao",
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
  "validacao": true
}
```

---

# Tratamento de Erros

## Erros de Entrada

| Código             | Descrição                  |
| ------------------ | -------------------------- |
| ARQUIVO_AUSENTE    | Nenhum arquivo foi enviado |
| PDF_INVALIDO       | Arquivo não é PDF válido   |
| CATEGORIA_INVALIDA | Categoria não reconhecida  |

## Erros de Processamento

| Código             | Descrição                                 |
| ------------------ | ----------------------------------------- |
| TEXTO_NAO_EXTRAIDO | Falha na leitura do PDF                   |
| ANALISE_INCOMPLETA | Nem todas as categorias foram processadas |
| ERRO_FERRAMENTA    | Uma ferramenta falhou durante execução    |

---

# Critérios para Identificar Respostas Incompletas

Uma resposta será considerada incompleta quando:

* Nem todas as categorias solicitadas forem processadas;
* Alguma ferramenta retornar erro;
* O texto não puder ser extraído;
* Campos obrigatórios estiverem ausentes;
* O relatório final não puder ser gerado.

Exemplo:

```json
{
  "validacao": false,
  "motivo": "Categoria solicitada não processada."
}
```

---

# Limites da IA

A IA pode:

* Identificar elementos estruturais do documento;
* Localizar referências bibliográficas;
* Detectar possíveis erros ortográficos;
* Produzir relatórios de análise;
* Sinalizar inconsistências encontradas.

A IA NÃO pode:

* Aprovar formalmente trabalhos acadêmicos;
* Atribuir notas finais;
* Garantir conformidade completa com normas ABNT;
* Avaliar qualidade científica do conteúdo;
* Substituir a revisão humana;
* Inventar informações ausentes no documento.

Quando houver incerteza ou ausência de dados, o sistema deverá registrar a ocorrência e solicitar revisão humana.

---

# Checklist de Validação

* [x] O grupo definiu o formato das entradas.
* [x] O grupo definiu o formato das saídas.
* [x] Há critérios para identificar erro, ausência de dado ou resposta incompleta.
* [x] Existem limites explícitos para o que a IA pode fazer.