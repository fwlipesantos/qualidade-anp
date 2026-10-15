# processos

## monitor_precos_anp

**finalidade:** avisar quando a carga de precos da ANP estiver atrasada

**janela de execucao:** a cada hora, alerta se a ultima carga com sucesso tiver mais de 8 dias

**responsavel:** Felipe Santos

**origem:** oracle.controle_arquivo

**destino:** alerta no telegram

```mermaid
flowchart LR
    "oracle.controle_arquivo" --> "alerta no telegram"
```

## precos_anp

**finalidade:** carregar os precos de combustiveis da ANP no modelo dimensional do Oracle, mantendo o historico dos postos

**janela de execucao:** segundas-feiras as 06:00, duracao esperada de ate 30 minutos

**responsavel:** Felipe Santos

**origem:** arquivo semestral da ANP (ca-AAAA-SS.csv)

**destino:** oracle.stg_preco, oracle.dim_produto, oracle.dim_municipio, oracle.dim_data, oracle.dim_posto, oracle.fato_preco, oracle.rejeitado_preco

```mermaid
flowchart LR
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.stg_preco"
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.dim_produto"
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.dim_municipio"
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.dim_data"
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.dim_posto"
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.fato_preco"
    "arquivo semestral da ANP (ca-AAAA-SS.csv)" --> "oracle.rejeitado_preco"
```
