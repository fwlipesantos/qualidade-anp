select count(*)
from fato_preco
where arquivo = :arquivo
  and (valor_venda is null or valor_venda <= 0)
