with atual as (
    select linhas, fim
    from controle_arquivo
    where arquivo = :arquivo
),
anteriores as (
    select avg(linhas) as media
    from (
        select c.linhas
        from controle_arquivo c, atual a
        where c.status = 'sucesso'
          and c.fim < a.fim
        order by c.fim desc
        fetch first 4 rows only
    )
)
select case
    when an.media is null then 0
    when abs(at.linhas - an.media) > 0.3 * an.media then 1
    else 0
end
from atual at, anteriores an
