# laboratório de incidentes

Falhas provocadas de propósito no ambiente local, para treinar e documentar a investigação de ponta a ponta. Nenhum destes casos aconteceu em produção: cada um tem o passo a passo para reproduzir, o sintoma, onde olhar, a causa e a correção.

| caso | onde a falha aparece | o que treina |
|---|---|---|
| [01 layout alterado](01-layout-alterado.md) | log do Airflow | seguir o erro por vários módulos até a origem |
| [02 consulta lenta](02-consulta-lenta.md) | Oracle | ler o plano de execução |
| [03 segredo errado em hml](03-segredo-errado.md) | status do pod e log | operar variáveis e segredos no Rancher |
