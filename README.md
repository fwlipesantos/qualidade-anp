# qualidade e confiabilidade dos dados

Checagens de qualidade, alertas, monitor de atraso, documentação dos processos e um laboratório de incidentes para o pipeline de preços da ANP.

Faz parte de um conjunto de três repositórios: [precos-anp](../precos-anp) (pipeline), **qualidade-anp** e [esteira-anp](../esteira-anp) (orquestração e entrega).

## checagens

Rodam depois de cada carga e ficam registradas em `resultado_qualidade`.

| checagem | severidade | o que verifica |
|---|---|---|
| `posto_com_duas_versoes_atuais` | crítica | o SCD2 não pode deixar um posto com duas versões atuais |
| `vigencia_sobreposta` | crítica | versões de um mesmo posto não podem se sobrepor no tempo |
| `preco_invalido_na_fato` | crítica | nenhum preço vazio, zerado ou negativo chegou na fato |
| `rejeitados_acima_do_limite` | aviso | mais de 5% do arquivo foi para a quarentena |
| `variacao_de_volume` | aviso | o volume variou mais de 30% contra a média dos últimos 4 arquivos |
| `dados_desatualizados` | aviso | a coleta mais recente tem mais de 15 dias |

**Crítica** interrompe a execução: a DAG falha e o alerta dispara. **Aviso** deixa a execução seguir e manda alerta. Cada checagem é um arquivo SQL em `sql/checagens` que devolve o número de problemas, então adicionar uma nova é criar o SQL e uma linha em `qualidade/checagem.py`.

## alertas

A classe `Alerta` manda mensagem no Telegram, sempre com o ambiente na frente (`[prod] falha em precos_anp.carregar_arquivo`). Sem token configurado, ela só registra no log e não quebra nada, o que é útil em dev.

São três tipos de alerta:

- **falha**: qualquer tarefa que falhou depois dos retries, com a DAG, a tarefa, a tentativa e o erro
- **atraso**: o `MonitorAtraso` avisa quando a última carga com sucesso passou do limite
- **volume**: a checagem de variação de volume

## fichas dos processos

Cada processo tem uma ficha em `processos/` com finalidade, origem, destino, janela de execução e responsável. O gerador monta a documentação com o mapa de linhagem:

```bash
python gerar_documentacao.py
```

O resultado fica em [docs/processos.md](docs/processos.md). O ci do `esteira-anp` falha se existir DAG sem ficha.

## laboratório de incidentes

Falhas provocadas de propósito, com o passo a passo da investigação: sintoma, onde olhar, causa e correção por pull request. Veja [incidentes/](incidentes/README.md).

## testes

```bash
pip install -r requirements.txt
pytest
```
