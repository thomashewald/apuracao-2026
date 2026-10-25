@echo off
rem Testa se as URLs do TSE respondem (200 = ok)
set B=https://resultados.tse.jus.br/oficial
for %%U in (
  comum/config/ele-c.json
  ele2026/6258/dados/br/br-c0001-e006258-u.json
  ele2026/6258/dados/br/br-e006258-ab.json
) do (
  echo %%U
  curl -s -o nul -w "  HTTP %%{http_code}\n" -A "Mozilla/5.0" "%B%/%%U"
)
pause
