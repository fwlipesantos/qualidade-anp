# 01 layout alterado

## como reproduzir

Copie a amostra do projeto precos-anp e troque o nome da coluna `CNPJ da Revenda` por `Documento`. Rode a DAG `precos_anp` apontando para esse arquivo.

## sintoma

A tarefa `carregar_arquivo` falha nas três tentativas, e chega o alerta de falha com a mensagem `colunas obrigatorias ausentes: cnpj`.

## onde olhar

1. **log da tarefa no Airflow**: o rastreamento mostra o caminho da execução de baixo para cima:
   `tarefas.precos_anp.carregar_arquivo` → `anp.pipeline.Pipeline.processar` → `anp.leitor.LeitorArquivo.ler`
2. **controle_arquivo no Oracle**: o arquivo aparece com `status = 'erro'` e a mesma mensagem.
   ```sql
   select arquivo, status, mensagem, inicio from controle_arquivo order by inicio desc
   ```
3. **fato_preco**: nenhuma linha nova com esse arquivo, porque a carga é tudo ou nada.

## causa

A fonte mudou o nome de uma coluna obrigatória. O `LeitorArquivo` recusa o arquivo em vez de carregar errado.

## correção

Em uma branch, adicionar `"documento": "cnpj"` no mapa do `LeitorArquivo` e um teste com esse layout. Abrir pull request, passar pelo dev e pela homologação e só então promover para produção. Depois, reprocessar o arquivo com o parâmetro `reprocessar`.

## o que este caso mostra

A falha acontece três camadas abaixo de onde aparece. Ler o rastreamento de baixo para cima leva direto ao módulo certo, sem precisar mexer no ambiente.
