select count(*)
from (
    select cnpj
    from dim_posto
    where atual = 'S'
    group by cnpj
    having count(*) > 1
)
