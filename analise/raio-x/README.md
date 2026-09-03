# Raio-X do escalonamento — parte 1 (Slack)

Censo do canal `#ask-retail-priority` entre 03/06 e 03/09/2026.

## Arquivos

- `all.tsv` — extração bruta: 314 threads (ts, nº de respostas, última resposta, autor, título).
- `proc.py` — pseudonimização, classificação e métricas. Roda com `python3 proc.py all.tsv`.
- `dataset-anon.json` — dataset processado **sem o título bruto**, porque os títulos
  contêm telefone de cliente em texto aberto.

## Dados pessoais

`all.tsv` contém telefones nos títulos. O `proc.py` converte cada telefone num
identificador derivado por hash (`CLI-xxxxxx`) usando um salt local, e nenhum
número aparece em saída ou em material publicado.

**Antes de versionar em repositório compartilhado, avaliar se `all.tsv` deve
ficar fora** — ele é a única peça com dado pessoal em claro.

## Método

Três camadas com confiabilidade diferente:

1. **Censo estrutural** (303/303) — volume, motivo, tipo, urgência, duração, recorrência.
2. **Busca dirigida** (canal inteiro) — contagem de desfechos por expressão; é piso, não teto.
3. **Leitura profunda** (6 threads) — cadeia de repasses e modos de falha. Amostra
   escolhida entre os casos difíceis: descreve mecanismo, não mede frequência.

Duração = do post até a última mensagem da thread. Não é tempo de resolução.
O relógio começa quando o CS postou — a espera anterior, na central, não está
instrumentada.
