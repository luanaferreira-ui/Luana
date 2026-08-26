# Registro — decisões, riscos e perguntas em aberto

Atualizado em 26/ago/2026. Arquivo vivo: toda decisão tomada no touchpoint entra
aqui com data e dono; um risco só sai quando vira decisão ou deixa de existir.

## Decisões já tomadas

| # | Decisão | Data | Quem |
|---|---|---|---|
| D1 | O projeto tem dois blocos: **Estruturação** (Luana) e **Operação** (Luiza) | 26/ago | Luana + Luiza |
| D2 | O alvo é o **long tail regional**; o corporate segue com o time interno | 26/ago | Luana + Luiza |
| D3 | **Franquia sai** como caminho preferencial — a lei obriga a remunerar o franqueado por qualquer varejo da região, mesmo fora da carteira dele | 26/ago | Luana + Luiza |
| D4 | **Representação comercial** é o modelo mais provável (referência DTX/Imperium) | 26/ago | Luana + Luiza |
| D5 | A remuneração se ancora em **CAC / novos clientes**, com componente de recorrência a definir — não em originação total pura | 26/ago | Luana + Luiza |
| D6 | Cadastro de lojas e operadores **fica com o time da Amanda** no curto prazo, por segurança; automatizar é backlog | 26/ago | Luana + Luiza |
| D7 | O representante é **dono do resultado da carteira**, com autonomia de execução — sem microgerenciamento | 26/ago | Luana + Luiza |
| D8 | Primeiro se desenha **o quê**, depois se adapta ao **como** dos modelos de mercado | 26/ago | Luana + Luiza |
| D9 | **Google Sheets é a fonte de verdade** do projeto; o Painel de Demandas fica com o dia a dia | 26/ago | Luana |
| D10 | Setembro entrega **o modelo escolhido e defendido** — remuneração e contrato vêm depois, em fase própria | 26/ago | Luana |
| D11 | O piloto vai a campo em **11/jan/2027**, não em dezembro, para não ler resultado em cima do pico | 26/ago | Luana |

## Riscos

Os cinco primeiros são os que entram no status do Lucas.

| # | Risco | Prob. | Impacto | Sinal de alerta antecipado | Mitigação | Dono |
|---|---|---|---|---|---|---|
| R1 | Remuneração mal calibrada: pagar sobre originação total estoura o CAC e o modelo deixa de se pagar | Alta | Alto | No 1º cenário modelado, o custo por novo cliente passa de R$ 14 sem contrapartida de volume | Ancorar em CAC/novos clientes com guardrails de FPD e MOIC, teto por carteira e revisão a cada 6 meses | Luana |
| R2 | Uma restrição jurídica invalida o modelo depois de desenhado | Média | Alto | O direcional do Thiago (T2.3) vem com "depende" em vez de "pode/não pode" | Direcional mínimo antes de modelar; três cenários levados ao parecer, não um | Luana |
| R3 | Escopo infla — engajamento, prospecção de varejo e comercial no mesmo pacote | Alta | Alto | Aparece tarefa de rebate ou MDR no tracker sem decisão de gate | Fora de escopo assinado na F1; prospecção só entra se a Q1 virar sim, e mesmo assim fora do piloto | Luana |
| R4 | As 8h/semana não se sustentam quando a operação do dia a dia aperta | Alta | Alto | Duas semanas seguidas com menos de 5h apontadas, ou touchpoint desmarcado duas vezes | Bloco de sexta protegido; abaixo de 5h corta-se P2 antes de empurrar P0; capacidade revista no status quinzenal | Luiza |
| R5 | Cadastro e acessos presos no time da Amanda viram o gargalo da operação terceirizada | Média | Médio | Qualquer pedido de acesso do piloto levando mais de 48h | SLA escrito na T3.15, com fila visível; automação vira backlog de Tech antes da onda 2 | Luiza |
| R6 | O atendimento não resolve e tudo volta para a UME por caminho informal (N2 de fato) | Média | Médio | O representante manda a primeira mensagem direta pedindo suporte de cliente | Fluxo de exceção explícito, canal único e volume medido no piloto | Luiza |
| R7 | Não existe leitura confiável de CAC real (o projeto da Mandinha aponta ~30% na Polishop, com pessoas e viagens) | Média | Médio | O business case fica sensível demais a uma premissa não medida | Usar os R$14 como âncora declarada e revisar quando o projeto da Mandinha fechar | Luana |
| R8 | Exigir uniforme, jornada ou rotina do representante cria risco de vínculo trabalhista | Média | Alto | Alguma minuta ou guia usa "deve" em vez de "recomendamos" | Comportamento vira **recomendação de boas práticas**, nunca obrigação contratual | Luiza |
| R9 | O parceiro negocia fora da alçada (limite, juros, MDR) achando que representa a UME | Média | Médio | Primeira negociação em que ele promete condição que não temos | Matriz de alçadas (T3.5) escrita no contrato, com o que sobe para a UME | Luana |

## Perguntas em aberto

| # | Pergunta | Decidir até | Quem responde |
|---|---|---|---|
| Q1 | O representante **prospecta novos varejos** ou só atua nos existentes? Define se precisamos de rebate/MDR para ele | Gate F2 (25/set) | Lucas |
| Q2 | Qual o **nome do modelo**? "Modelo de engajamento" não cobre prospecção | Gate F2 (25/set) | Luana + Luiza |
| Q3 | O componente de recorrência amarra em **originação total, base ativa ou consulta**? | Gate F3 (30/out) | Luana + Financeiro |
| Q4 | O pacote tem **custo fixo/retainer** ou é 100% variável? | Gate F3 (30/out) | Luana + Financeiro |
| Q5 | Até onde vai o **uso da marca** pelo representante sem criar risco trabalhista? | Gate F3 (30/out) | Jurídico |
| Q6 | Quem é o **dono do modelo dentro da UME** — a pessoa única que destrava? | Gate F4 (18/dez) | Lucas |
| Q7 | A estrutura DTX/Imperium que já roda entra como **piloto zero** ou começamos do zero? | Gate F4 (18/dez) | Luana |
| Q8 | Qual a **frequência da agenda de alinhamento** com o representante? | Gate F3 (30/out) | Luiza |
