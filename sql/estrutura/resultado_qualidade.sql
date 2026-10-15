create table resultado_qualidade (
    arquivo       varchar2(100),
    checagem      varchar2(100),
    severidade    varchar2(20),
    problemas     number,
    aprovado      char(1),
    verificado_em timestamp default systimestamp
)
