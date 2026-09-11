# Lista de contatos — `contatos.csv`

337 contatos distintos, identificados por hash. Nenhum número em claro.

## Colunas

| coluna | o que é |
|---|---|
| `contato_id` | `CT-` + hash do telefone (mesmo salt do resto do projeto) |
| `tipo` | cliente · varejo · institucional · indefinido (ver abaixo) |
| `varejo` | quando conhecido. Só o WhatsApp identifica, pelo grupo |
| `canais` | slack · whatsapp · **ambos** |
| `n_slack` / `n_whatsapp` | ocorrências em cada canal |
| `primeiro` / `ultimo` | janela de aparição |
| `motivos` | motivos classificados, separados por `\|` |

## Como o tipo é inferido

| tipo | regra | n |
|---|---|---:|
| `cliente` | título do Slack diz "atendimento ao cliente" | 131 |
| `cliente (citado pelo varejo)` | telefone citado no texto de um grupo — o cliente não fala no grupo, o vendedor fala dele | 87 |
| `varejo` | título do Slack diz "atendimento ao varejo / vendedor / lojista" | 67 |
| `varejo (participante do grupo)` | autor de mensagem identificado por telefone no export | 23 |
| `institucional / canal divulgado` | aparece em 3+ grupos, ou é fixo de capital — é canal da Ume, não pessoa | 11 |
| `indefinido` | sem marcador no título | 9 |

## Limites que importam para o cruzamento

- **O varejo só é conhecido no lado WhatsApp** (126 de 337). O título do Slack
  raramente nomeia a loja.
- **`cliente (citado pelo varejo)` é inferência**, não declaração. O telefone
  aparece no texto; assumimos ser do cliente porque o vendedor está falando dele.
- **Apenas 5 contatos aparecem nos dois canais** — todos do Sipolatti, todos com
  motivo de pagamento. Não é amostra: é indício de que o mesmo caso circula, e de
  que a maioria das demandas não carrega telefone (98,4% das do WhatsApp não têm).
- `motivos = outros` em 117 contatos: o título ou a mensagem não trazem tema
  reconhecível.

## Para cruzar com a base da central

Hashear o telefone da central com o mesmo salt e dar `JOIN` por `contato_id`.
O script `colher.py` tem a função. O salt está no código — trocar antes de
qualquer uso fora deste projeto.
