select case
    when max(data_coleta) < trunc(sysdate) - 15 then 1
    else 0
end
from fato_preco
