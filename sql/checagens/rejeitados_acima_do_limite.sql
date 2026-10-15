select case
    when rejeitadas > 0.05 * (linhas + rejeitadas) then 1
    else 0
end
from controle_arquivo
where arquivo = :arquivo
