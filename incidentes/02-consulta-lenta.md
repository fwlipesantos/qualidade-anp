# 02 consulta lenta

## como reproduzir

Carregue alguns semestres na `fato_preco` e rode a consulta abaixo, que filtra a data com uma função:

```sql
select avg(valor_venda)
from fato_preco
where to_char(data_coleta, 'YYYY-MM') = '2024-03'
```

## sintoma

A consulta demora muito mais que o esperado para um único mês.

## onde olhar

Gerar o plano de execução:

```sql
explain plan for
select avg(valor_venda)
from fato_preco
where to_char(data_coleta, 'YYYY-MM') = '2024-03'

select * from table(dbms_xplan.display)
```

No plano, observar a coluna `Pstart` e `Pstop`. Com a função aplicada na coluna, o Oracle não consegue saber qual partição ler e percorre todas (`PARTITION RANGE ALL`).

## causa

A `fato_preco` é particionada por mês em `data_coleta`. Aplicar `to_char` na coluna esconde o valor da data do otimizador e desliga o descarte de partições.

## correção

Filtrar a coluna diretamente, por intervalo:

```sql
explain plan for
select avg(valor_venda)
from fato_preco
where data_coleta >= date '2024-03-01'
  and data_coleta <  date '2024-04-01'

select * from table(dbms_xplan.display)
```

O plano passa a mostrar `PARTITION RANGE SINGLE`: só a partição de março é lida.

## registro

Cole aqui os dois planos gerados no seu ambiente, com o tempo de cada consulta, para comparar antes e depois.
