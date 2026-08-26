# Modelo de Terceirização da Operação — UME

Projeto estruturado a partir da reunião **"Escalabilidade time"** (Luiza Falcone
e Luana Ferreira, 26/ago/2026) e das anotações do quadro. Patrocinador: **Lucas**.

**Resumo em cinco linhas.** A UME não consegue atender os varejos menores com o
time interno, e esses varejos ficam sem dono. O projeto desenha, contrata e
testa um modelo de terceirização da operação do **long tail regional**, para que
o time interno se concentre nos varejos corporate. São cinco fases sequenciais,
cada uma com um dono único: enquadramento (set), escolha do modelo (30/set),
desenho de remuneração e contrato (13/nov), prontidão operacional (18/dez) e
piloto assistido com decisão de escalar em **16/abr/2027**. A Luana responde
pelas fases de estruturação, a Luiza pelas de operação; ambas trabalham em todas
as fases. Com **8h/semana de cada uma**, o plano fecha — mas as semanas de
setembro e outubro ficam 100% ocupadas, sem folga para imprevisto.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| **Tracker (fonte única de verdade)** | [Google Sheets — Tarefas](https://docs.google.com/spreadsheets/d/1-c780Jo_bP9d-xMW0qYGu_Q2hw0ECICEsNPtCrQXHSg/edit) |
| **Dia a dia / baixa das demandas** | Painel de Demandas (`localhost:4321`), cluster **Novos Negócios**, conta **Terceirização** |
| Plano estruturado (fases, tarefas, dependências, carga) | [`plano.json`](plano.json) |
| Decisões, riscos e perguntas em aberto | [`registro.md`](registro.md) |
| Tracker completo em planilha (12 abas, views prontas) | [`tracker-terceirizacao.xlsx`](tracker-terceirizacao.xlsx) |
| Linhas prontas para o Painel | [`demandas-painel.jsonl`](demandas-painel.jsonl) |

Para regerar tudo depois de mexer no plano: `python3 gerar_plano.py && python3 agendar.py && python3 gerar_tracker.py`.

## 1. Escopo fechado

### Dentro

- Desenhar e escolher o modelo de terceirização da operação do long tail regional
- Validar juridicamente o modelo e o formato de remuneração
- Definir remuneração, regras de apuração e business case
- Redigir a minuta de contrato e a matriz de alçadas do representante
- Montar o onboarding do representante e o do varejo, tocado por ele
- Especificar e publicar o dash de operação e o dash financeiro, com export CSV
- Publicar repositório de trade, brand book, FAQ e canais de atendimento
- Selecionar e contratar **um** parceiro para o piloto
- Rodar o piloto por 3 ciclos de apuração e recomendar escalar, ajustar ou encerrar

### Fora — não faremos agora

- Terceirizar varejo corporate: segue com o time interno
- Prospecção e venda de novos varejos pelo representante (ver Q1 no registro) — fora do piloto de qualquer forma
- Rebate e MDR para o representante: só existe se a Q1 virar sim
- Automatizar o cadastro de lojas e operadores: fica com o time da Amanda e vira backlog de Tech
- Franquia e licenciamento de marca: descartados em 26/ago
- Criar um time interno de N2 dedicado ao canal terceirizado
- Mexer em política de crédito, alçadas de aprovação ou qualquer coisa em produção
- Onda 2 de representantes e expansão nacional: só depois do Gate 5
- Uniforme ou identidade obrigatória para o representante: vira recomendação, por risco de vínculo

### Definição de pronto

O projeto acabou quando: existe um representante terceirizado rodando uma
carteira long tail com contrato assinado; a remuneração foi apurada e paga por
3 ciclos, com o business case real medido contra o modelado; o playbook está
publicado e foi usado por alguém de fora da UME; o time interno consegue mostrar
com número quantas horas por semana deixou de gastar com esses varejos; e a
recomendação de escalar, ajustar ou encerrar foi decidida com o Lucas.

### Métricas de sucesso

| # | Métrica | Baseline hoje | Meta | Dono | Onde se mede |
|---|---|---|---|---|---|
| M1 | Horas/semana do time interno gastas com varejo long tail | **A medir** na F1 (amostra de 2 semanas) | −60% até o fim do piloto | Luana | Apontamento das duas + agenda |
| M2 | Varejos ativos sob carteira terceirizada | 0 | 10 a 15 lojas no piloto | Luiza | Dash de operação |
| M3 | CAC do canal terceirizado (R$/novo cliente) | R$ 14 (referência da central de vendas) | ≤ R$ 14, com teto de 2% sobre originação | Luana | Apuração mensal |
| M4 | FPD e inadimplência da carteira terceirizada | **A medir** (média UME por região) | Até 1 p.p. acima da média UME | Luana | Risco / BigQuery |
| M5 | Originação da carteira-piloto vs. mesmo período do ano anterior | **A medir** na F4 | +15% no 3º ciclo | Luiza | Dash financeiro |

## 2. Fases

Cinco fases sequenciais. **Uma fase, um dono** — quem responde pelo critério de
saída. O apoio executa tarefas dentro da fase, mas não responde por ela.

| Fase | Dono | Apoio | Janela | Entregável | Critério de saída |
|---|---|---|---|---|---|
| **F1 · Enquadramento** | Luana | Luiza | 26/ago – 04/set | One-pager de escopo + régua de segmentação + tracker no ar | Escopo aprovado pelo Lucas, 4 métricas com baseline, tracker populado e cadência na agenda |
| **F2 · Descoberta e escolha do modelo** | Luana | Luiza | 08/set – 02/out | Comparativo de modelos com recomendação + direcional jurídico + baseline de CAC | **Um modelo escolhido e defendido**, red flags jurídicos conhecidos, inventário da operação levantado |
| **F3 · Desenho do modelo** | Luana | Luiza | 01/out – 13/nov | Remuneração escolhida + business case + minuta de contrato + guias e specs | Cenário escolhido entre 3, business case aprovado pelo Financeiro, parecer do Thiago, minuta pronta |
| **F4 · Prontidão operacional** | Luiza | Luana | 16/nov – 18/dez | Contrato assinado, dashboards no ar, guias publicados, representante certificado | Checklist de go/no-go assinado e ciclo de pagamento testado ponta a ponta |
| **F5 · Piloto assistido e decisão** | Luiza | Luana | 11/jan – 16/abr/27 | Piloto em campo + 3 apurações + recomendação ao Lucas | Recomendação entregue com leitura das hipóteses e do business case real |

**Caminho crítico** (a corrente mais longa; qualquer atraso aqui empurra a data final):

```
T2.1 direcional jurídico → T2.2 perguntas ao Thiago → T2.3 sessão com o Thiago
  → T2.8 recomendação de modelo → T3.1 árvore de métricas → T3.2 três cenários
  → T3.3 business case → T3.6 parecer jurídico → T3.7 minuta de contrato
  → T4.3 contrato assinado → T4.4 ciclo de pagamento testado → T4.11 go/no-go
  → T5.1 piloto em campo → T5.4 retrospectivas → T5.6 recomendação final
```

Repare que o caminho crítico **passa três vezes pelo jurídico e duas pelo
financeiro**. São as duas áreas que não controlamos e as duas que mais podem
atrasar o projeto. É por isso que o direcional jurídico mínimo (T2.1–T2.3) vem
antes de qualquer modelagem de remuneração: não faz sentido desenhar três
cenários se um deles é proibido.

**Dependências entre fases:** F2 depende de F1 (a régua de segmentação define o
que estamos comprando); F3 depende de F2 (não se modela remuneração sem modelo);
F4 depende de F3 (não se contrata sem contrato); F5 depende de F4 (não se vai a
campo sem checklist). Dentro das fases, as duas frentes correm em paralelo — a
Luiza levanta o inventário da operação enquanto a Luana fecha o modelo.

**Por que o piloto não vai a campo em dezembro:** dezembro é preparação,
treinamento e teste do ciclo de pagamento. O go-live é 11/jan para que o
resultado não seja lido em cima do pico de fim de ano.

## 3. Tarefas

Estão todas no [tracker](https://docs.google.com/spreadsheets/d/1-c780Jo_bP9d-xMW0qYGu_Q2hw0ECICEsNPtCrQXHSg/edit)
e em [`plano.json`](plano.json): 58 tarefas, cada uma com dono único, esforço em
horas, data alvo, dependência, prioridade e status inicial *Não iniciado*.
Nenhuma passa de 10h — todas cabem numa semana ou menos, exceto as tarefas
contínuas da F5, que são de calendário (o piloto roda no tempo dele).

**Prioridade:** **P0** sem ela o projeto não existe · **P1** importante, o
projeto sobrevive · **P2** melhora o resultado. Quando a semana apertar, corta
P2, depois P1. P0 nunca escorrega em silêncio.

Distribuição: 131h para a Luana, 162h para a Luiza, ao longo de 8 meses.

### Onde a conta não fecha

As datas do tracker **saíram de um agendador que respeita a capacidade de
8h/semana**, feriados incluídos — não são datas de desejo. Três coisas para
saber agora, e não em outubro:

1. **Setembro e outubro ficam com as duas 100% ocupadas.** De 07/set a 06/nov,
   quase toda semana usa as 8h inteiras das duas. Não existe folga para
   imprevisto: qualquer semana perdida empurra a data seguinte na mesma medida.
   Uma semana perdida na F2 atrasa a escolha do modelo; uma semana perdida no
   caminho crítico da F3 atrasa o contrato.
2. **A escolha do modelo cabe em setembro, mas raspando.** A recomendação (T2.8)
   fecha em **25/set** e duas tarefas P1 escorregam para 02/out: a ficha dos
   modelos alternativos e as conversas de referência. São insumos de
   comparação, não bloqueiam a decisão — mas significam que o comparativo do
   dia 25 sai com dois modelos bem estudados e um terceiro em rascunho.
   Para caber, já movi o levantamento de baseline de CAC (T2.7) para a Luiza,
   que é mais forte em dados, e empurrei duas tarefas de operação para a F3.
3. **[SUPOSIÇÃO] As 8h são de execução, e os rituais vêm por cima.** Touchpoints,
   status e comitê somam ~1h30/semana. Se os rituais tiverem que sair das 8h, a
   capacidade real vira 6h30 e a escolha do modelo escorrega cerca de uma semana
   — nesse caso o corte é T2.5 e T2.6 (as duas P1 acima), não uma P0.

A aba **Carga semanal** do `.xlsx` mostra semana a semana quanto sobra para cada uma.

## 4. Acompanhamento em tempo real

### O lugar único de verdade

**O Google Sheets é a fonte de verdade do projeto; o Painel de Demandas é onde
você dá baixa no dia a dia.** Quando os dois divergirem, o Sheets vence.

Por que o Sheets e não o Painel sozinho: o Painel foi feito para demandas soltas
de conta — não tem fase, prioridade, dependência nem visão de bloqueio, e o
projeto precisa dos quatro. Por que não só o Sheets: o seu hábito de dar baixa
já está no Painel, e um tracker que exige abrir uma segunda ferramenta para
marcar "feito" morre em três semanas. Então cada um faz o que já faz bem.

A ponte é automática: as tarefas das fases correntes já estão em
`radar-inbox.jsonl` e entram sozinhas no Painel no próximo `npm start`. Quando a
fase virar, rode `python3 gerar_plano.py` e copie o bloco seguinte de
`demandas-painel.jsonl` para a caixa do radar.

### Modelo de dados do tracker

| Campo | Valores | Quem preenche |
|---|---|---|
| ID | `T<fase>.<n>` | fixo |
| Fase | F1 a F5 | fixo |
| Tarefa | texto | fixo |
| Dono | Luana · Luiza | fixo, muda só por acordo no touchpoint |
| Prioridade | P0 · P1 · P2 | Luana, na revisão de fase |
| Esforço (h) | número | quem executa, ao reestimar |
| Data alvo | data | sai do agendador; mudar aqui é decisão, não ajuste |
| Dependência | IDs | fixo |
| **Status** | **Não iniciado · Em andamento · Bloqueado · Em revisão · Concluído** | quem executa |
| Bloqueio — motivo | texto | quem travou, **na hora** |
| Última atualização | data | quem mexeu |
| Áreas envolvidas | texto | fixo |

*Em revisão* quer dizer: o trabalho acabou e está com outra pessoa ou área.
Continua sendo seu até voltar.

### As quatro views

No `.xlsx` elas já vêm prontas. No Sheets, crie uma aba por view e cole a
fórmula (a aba de tarefas precisa se chamar `Tarefas`):

| View | Fórmula |
|---|---|
| Vence em 7 dias | `=SORT(FILTER(Tarefas!A2:L59; Tarefas!G2:G59<=HOJE()+7; Tarefas!I2:I59<>"Concluído"); 7; VERDADEIRO)` |
| Só bloqueios | `=FILTER(Tarefas!A2:L59; Tarefas!I2:I59="Bloqueado")` |
| Por dono | `=SORT(FILTER(Tarefas!A2:L59; Tarefas!D2:D59="Luana"; Tarefas!I2:I59<>"Concluído"); 7; VERDADEIRO)` |
| Por fase | filtro da coluna Fase na própria aba `Tarefas` |

### Ritual mínimo

| Ritual | Quando | Duração | Pauta |
|---|---|---|---|
| **Touchpoint** | terça e quinta | 30 min | 20 min de status, 10 min de desbloqueio. Só este assunto. |
| **Bloco protegido** | sexta de manhã | 2 h | Trabalho de fato. Fecha atualizando o tracker. |
| **Status para o Lucas** | quinzenal | 15 min | Uma página: andou, travou, precisa de decisão. |
| **Comitê de áreas** | mensal | 1 h | Jurídico, Financeiro, People/DP, CS e Dados na mesma sala. |
| **Revisão de fase** | no fim de cada fase | 1 h | Passa ou não passa, pelo critério escrito. |

**As duas regras que fazem isso funcionar:**

1. **Toda tarefa mexida no dia é atualizada antes de você sair.** Não na reunião — no dia.
2. **Bloqueio se registra na hora, com motivo escrito.** Bloqueio sem motivo escrito não conta como bloqueio.

### Resumo automático — segunda, 9h

Um resumo semanal cai no canal do projeto com quatro blocos: **o que andou** (o
que mudou de status na semana), **o que travou** (bloqueios abertos e há quantos
dias), **o que vence nos próximos 7 dias** e **o que precisa de decisão do
Lucas** (perguntas em aberto vencendo). Ele lê o tracker — se ninguém atualizar,
o resumo chega vazio, e isso também é informação.

| Atualizado por gente | Automático |
|---|---|
| Status, motivo do bloqueio, data de última atualização | As quatro views |
| Valor atual das métricas (M1 a M5) | O realce de data vencida |
| Reestimativa de esforço | As linhas para o Painel |
| Decisões e riscos novos no registro | O resumo de segunda |

### Métricas do próprio acompanhamento

Quatro números, lidos na sexta: entregas no prazo (%), tarefas bloqueadas (nº),
idade do bloqueio mais antigo (dias) e decisões pendentes (nº).

### Semáforo por frente

🟢 no prazo, nada bloqueado · 🟡 uma tarefa atrasada ou bloqueio com menos de 3
dias · 🔴 gate em risco, ou bloqueio com mais de 3 dias sem dono para destravar.

## 5. Riscos e escalonamento

| # | Risco | Prob. | Impacto | Sinal de alerta antecipado | Mitigação | Dono |
|---|---|---|---|---|---|---|
| R1 | Remuneração mal calibrada: pagar sobre originação total estoura o CAC | Alta | Alto | No 1º cenário modelado, o custo por novo cliente passa de R$ 14 sem contrapartida de volume | Ancorar em CAC/novos clientes, guardrails de FPD e MOIC, teto por carteira, revisão a cada 6 meses | Luana |
| R2 | Restrição jurídica invalida o modelo depois de desenhado | Média | Alto | O direcional do Thiago (T2.3) vem com "depende" em vez de "pode/não pode" | Direcional mínimo na F2, antes de modelar; três cenários levados ao parecer, não um | Luana |
| R3 | Escopo infla — engajamento, prospecção e comercial no mesmo pacote | Alta | Alto | Aparece tarefa de rebate ou MDR no tracker sem decisão de gate | Lista de fora de escopo assinada na F1; prospecção só entra se a Q1 virar sim | Luana |
| R4 | As 8h/semana não se sustentam quando a operação aperta | Alta | Alto | Duas semanas seguidas com menos de 5h apontadas, ou touchpoint desmarcado 2x | Bloco de sexta protegido; abaixo de 5h corta-se P2 antes de empurrar P0; capacidade revista no status quinzenal | Luiza |
| R5 | Cadastro e acessos presos no time da Amanda viram gargalo | Média | Médio | Qualquer pedido de acesso do piloto levando mais de 48h | SLA escrito na T3.15, fila visível; automação vira backlog de Tech antes da onda 2 | Luiza |

### Regra de escalonamento

1. **Na hora:** o bloqueio é registrado no tracker, com motivo.
2. **48h:** vira pauta obrigatória do touchpoint seguinte.
3. **3 dias úteis:** sobe para o Lucas com a decisão pedida por escrito — o que
   está travado, quem destrava, o que acontece se não destravar.
4. **Risco de gate:** se o bloqueio ameaça a data de um gate, sobe na hora, sem
   esperar os 3 dias.

Bloqueio de área externa (Jurídico, Financeiro, Dados) que não se resolve em 5
dias úteis entra na pauta do comitê mensal ou antecipa o comitê.

## Suposições que assumi

- **[SUPOSIÇÃO]** As 8h/semana são de execução; os rituais (~1h30) vêm por cima.
- **[SUPOSIÇÃO]** Jurídico, Financeiro e Dados respondem em até 5 dias úteis.
- **[SUPOSIÇÃO]** O piloto é uma região, com 10 a 15 lojas.
- **[SUPOSIÇÃO]** Recesso de 21/dez a 08/jan sem trabalho de projeto; feriados nacionais considerados.
- **[SUPOSIÇÃO]** O Lucas decide; CS, People e Financeiro acompanham e são consultados.
- **[SUPOSIÇÃO]** Nada em produção é alterado, e o cadastro segue com o time da Amanda durante todo o piloto.

## Origem

Reunião **Escalabilidade time**, 26/ago/2026, 11h31 — Luiza Falcone e Luana
Ferreira. Notas no Granola e foto das anotações do quadro. Os dois blocos
(Estruturação e Operação), a lista de métricas de remuneração, as duas personas
de onboarding e a separação onboarding/ongoing vêm direto do quadro; fases,
datas, capacidade e governança foram construídas a partir dele.
