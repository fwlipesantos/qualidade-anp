select count(*)
from dim_posto a
join dim_posto b
    on a.cnpj = b.cnpj
   and a.id_posto < b.id_posto
   and a.valido_de <= nvl(b.valido_ate, date '9999-12-31')
   and b.valido_de <= nvl(a.valido_ate, date '9999-12-31')
