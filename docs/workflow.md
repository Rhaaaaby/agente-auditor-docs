# Workflow Agêntico

## Projeto

**Agente Auditor de Documentos Configurável**

---

# Objetivo

Receber um documento acadêmico, executar verificações conforme as categorias selecionadas pelo usuário e gerar um relatório estruturado contendo os resultados da análise.

---

# Entrada do Workflow

O workflow recebe:

* Arquivo PDF;
* Categorias de análise selecionadas.

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

# Fluxo Geral

```text
Upload PDF
    ↓
Validação da Entrada
    ↓
Extração de Texto
    ↓
Planejamento das Ações
    ↓
Execução das Ferramentas
    ↓
Consolidação dos Resultados
    ↓
Validação
    ↓
Relatório Final
```

---

# Etapa 1 — Validação da Entrada

## Objetivo

Garantir que os dados necessários para execução do workflow foram fornecidos.

## Processamento

* Verificar existência do arquivo;
* Verificar formato PDF;
* Verificar se existe ao menos uma categoria selecionada.

## Saída

```json
{
  "arquivo_valido": true,
  "categorias": [
    "estrutura",
    "referencias",
    "ortografia"
  ]
}
```

---

# Etapa 2 — Extração de Texto

## Objetivo

Obter o conteúdo textual do documento.

## Processamento

* Abrir o PDF;
* Extrair texto de todas as páginas;
* Consolidar o conteúdo.

## Saída

```json
{
  "texto_extraido": "conteudo do documento"
}
```

---

# Etapa 3 — Planejamento das Ações

## Objetivo

Determinar quais ferramentas deverão ser utilizadas.

## Processamento

* Ler categorias solicitadas;
* Selecionar ferramentas correspondentes;
* Ignorar verificações não solicitadas.

## Saída

```json
{
  "acoes": [
    "verificar_estrutura",
    "verificar_referencias",
    "verificar_ortografia"
  ]
}
```

---

# Etapa 4 — Execução das Ferramentas

## Objetivo

Executar as verificações solicitadas.

### Ferramenta: verificar_estrutura

Verifica:

* Introdução;
* Desenvolvimento;
* Conclusão.

Saída:

```json
{
  "categoria": "estrutura",
  "introducao": true,
  "desenvolvimento": true,
  "conclusao": false
}
```

### Ferramenta: verificar_referencias

Verifica:

* Existência de referências;
* Quantidade encontrada.

Saída:

```json
{
  "categoria": "referencias",
  "quantidade": 8
}
```

### Ferramenta: verificar_ortografia

Verifica:

* Possíveis erros ortográficos.

Saída:

```json
{
  "categoria": "ortografia",
  "erros": 12
}
```

---

# Etapa 5 — Consolidação dos Resultados

## Objetivo

Unificar os resultados produzidos pelas ferramentas.

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

# Etapa 6 — Validação

## Objetivo

Garantir que todas as verificações solicitadas foram executadas.

## Processamento

* Comparar categorias solicitadas com categorias processadas;
* Detectar falhas de execução;
* Confirmar integridade do relatório.

## Saída

```json
{
  "validacao": true,
  "categorias_solicitadas": 3,
  "categorias_processadas": 3
}
```

---

# Etapa 7 — Relatório Final

## Objetivo

Entregar o resultado consolidado para o usuário.

## Saída Final

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
  }
}
```

---

# Critérios de Avaliação

O resultado será considerado adequado quando:

1. O PDF for processado corretamente;
2. O texto for extraído sem erros;
3. Todas as categorias selecionadas forem executadas;
4. O relatório final for gerado;
5. Os resultados forem estruturados e legíveis;
6. A validação retornar valor verdadeiro.

---

# Checklist de Validação

* [x] A entrada do workflow está definida.
* [x] As etapas do workflow estão em ordem lógica.
* [x] A saída de cada etapa está clara.
* [x] A saída final está definida.
* [x] Existe pelo menos um critério para avaliar se o resultado ficou adequado.