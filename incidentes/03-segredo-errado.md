# 03 segredo errado em hml

## como reproduzir

No ambiente de homologação, atualize o segredo do Oracle com uma senha errada:

```bash
./scripts/segredos.sh hml   # usando um .env.hml com oracle_senha incorreta
```

Rode a DAG `precos_anp` em hml.

## sintoma

A tarefa `preparar_estrutura` falha logo no início com `ORA-01017: invalid credential or not authorized`.

## onde olhar

1. **log da tarefa no Airflow**: o erro acontece na criação da conexão, em `anp.banco.Banco`.
2. **status do pod**: com o KubernetesExecutor cada tarefa roda num pod próprio.
   ```bash
   kubectl -n airflow-hml get pods
   kubectl -n airflow-hml describe pod <pod-da-tarefa>
   ```
3. **segredo em uso**: conferir as chaves sem expor os valores.
   ```bash
   kubectl -n airflow-hml get secret anp-oracle -o jsonpath='{.data}' | tr ',' '\n' | cut -d: -f1
   ```

## causa

O segredo `anp-oracle` de homologação foi atualizado com a senha errada. O código não mudou, só a configuração do ambiente.

## correção

Corrigir o `.env.hml`, reaplicar o segredo e reiniciar os componentes de forma controlada:

```bash
./scripts/segredos.sh hml
./scripts/reiniciar.sh hml
```

## o que este caso mostra

Nem toda falha é de código. Separar configuração de código, com segredos por ambiente, faz a correção ser só no ambiente afetado, sem deploy e sem tocar em produção.
