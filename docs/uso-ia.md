# Uso da IA

## Projeto

**Agente Auditor de Documentos Configurável**

---

# Objetivo da IA no Projeto

A Inteligência Artificial será utilizada para auxiliar na análise preliminar de documentos acadêmicos, executando tarefas de interpretação textual e identificação de padrões que seriam demoradas de realizar manualmente.

A IA não será responsável pela aprovação ou reprovação de documentos. Sua função é apoiar o processo de revisão por meio da geração de análises e relatórios estruturados.

---

# Função Operacional da IA

A IA possui uma função operacional claramente definida:

* Interpretar o conteúdo textual extraído do documento;
* Identificar elementos estruturais;
* Localizar possíveis referências bibliográficas;
* Detectar possíveis inconsistências;
* Produzir relatórios explicativos;
* Justificar os resultados encontrados.

A IA atua como um agente analista dentro do workflow.

---

# Etapas do Workflow em que a IA Será Utilizada

## Etapa 1 – Planejamento das Ações

A IA recebe as categorias selecionadas pelo usuário e determina quais verificações deverão ser executadas.

Exemplo:

Categorias recebidas:

```json
{
  "categorias": [
    "estrutura",
    "ortografia"
  ]
}
```

Resultado esperado:

```json
{
  "acoes": [
    "verificar_estrutura",
    "verificar_ortografia"
  ]
}
```

---

## Etapa 2 – Análise Estrutural

A IA interpreta o texto extraído para identificar a presença de elementos como:

* Introdução;
* Desenvolvimento;
* Conclusão;
* Referências.

A decisão é baseada no conteúdo efetivamente encontrado no documento.

---

## Etapa 3 – Geração de Justificativas

Além de retornar resultados estruturados, a IA produz explicações curtas sobre os problemas encontrados.

Exemplo:

```json
{
  "categoria": "estrutura",
  "resultado": "incompleto",
  "justificativa": "A seção de conclusão não foi identificada."
}
```

---

# Etapas Sem Uso de IA

As seguintes etapas são executadas por regras e código tradicional:

* Upload do arquivo;
* Validação do formato PDF;
* Extração de texto;
* Controle do fluxo;
* Consolidação dos resultados;
* Validação final do relatório.

Essas etapas não dependem de modelos de linguagem.

---

# Decisão Final e Supervisão Humana

A decisão final permanece sob responsabilidade humana.

A IA não possui autorização para:

* Aprovar trabalhos acadêmicos;
* Reprovar trabalhos acadêmicos;
* Atribuir notas;
* Tomar decisões administrativas;
* Certificar conformidade total com normas acadêmicas.

O sistema apenas fornece recomendações e evidências para auxiliar a revisão.

Sempre que houver:

* Baixa confiança;
* Informações insuficientes;
* Resultado inconsistente;
* Erro de processamento;

o documento deverá ser encaminhado para revisão humana.

---

# Tratamento de Ambiguidade

Quando a IA não conseguir determinar um resultado com segurança suficiente, deverá retornar um estado de incerteza.

Exemplo:

```json
{
  "categoria": "estrutura",
  "status": "revisao_humana",
  "motivo": "Não foi possível confirmar a presença da conclusão."
}
```

Nesses casos, nenhuma decisão automática será tomada.

---

# Dependência da IA

O projeto não depende exclusivamente de uma conversa livre com chatbot.

A IA está integrada a um workflow controlado que possui:

* Entradas definidas;
* Contratos de dados;
* Ferramentas específicas;
* Critérios de validação;
* Tratamento de erros;
* Limites operacionais.

O modelo de linguagem é apenas um componente do processo.

---

# Benefícios Esperados

* Redução do tempo de revisão inicial;
* Padronização das verificações;
* Melhoria da rastreabilidade das análises;
* Apoio à tomada de decisão humana;
* Diminuição de tarefas repetitivas.

---

# Checklist de Validação

* [x] A IA tem uma função operacional clara.
* [x] O grupo sabe em quais etapas a IA será usada.
* [x] A decisão final continua com pessoa responsável quando houver risco ou ambiguidade.
* [x] O projeto não depende apenas de uma conversa livre com chatbot.