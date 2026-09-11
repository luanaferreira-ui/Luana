# Leitura dos prints — achados (parcial: 9 de 73 lidas)

Regra de PII: nenhum nome, CPF ou telefone reproduzido. Casos identificados por hash.

## A1. A central declara SLA de 12 horas úteis
Print 03/07 17:24 (Sipolatti) — conversa com **Ume – Atendimento ao Varejo** (canal verificado):
> "Prazo de conclusão: A solicitação será encaminhada para análise e poderá ser
> concluída em até 12 horas úteis, após o envio completo das informações."
Conversa original de 11/jun; print postado no grupo em 03/jul, com o varejista
mandando "oi" às 17:24 sem resposta. **22 dias depois, ainda tentando.**

## A2. Regra de acesso que causa o ping-pong de senha
Mesmo print:
> "Por medida de segurança, somente o gerente pode solicitar acesso para a loja.
> Peça para ele entrar em contato através do número cadastrado e clicar na opção
> 'Cadastrar Operador'"
Casa com a pergunta sem resposta no Slack (16/06) sobre reset de senha circular
entre central do varejo e central do cliente.

## A3. O bot atende fora do horário e NÃO resolve — e oferece renegociação
Print 02/09 09:24 (Sipolatti) — **Ume – Apoio Financeiro** (canal verificado), 08:40:
> "Como nossa equipe humana está fora do horário de atendimento, não consigo
> verificar o que aconteceu com o pagamento feito há mais de um mês."
> "Posso te ajudar com outra coisa que esteja ao meu alcance, como gerar um boleto
> para a próxima parcela ou para quitar sua dívida, ou iniciar um processo de
> renegociação?"
RISCO: cliente que pagou e segue cobrado recebe oferta de quitar dívida ou renegociar.
Às 08:40 de um dia útil o canal se declara fora do horário humano.

## A4. Caso completo ponta a ponta, 3 canais, 30 dias (CLI recorrente, Sipolatti)
- 01/08  vencimento da parcela
- 03/08  pagamento em dinheiro no banco (comprovante fotografado)
- 19/08 09:33  varejo posta comprovante no grupo: "mais de 15 dias e nao deram baixa";
        "No atendimento fica só mandando mensagem automática"; "Não consegui resolver por lá"
- 01/09 08:55  MESMO cliente volta à loja. Varejo: "clientes que pagam no sábado estão
        sendo cobrados indevidamente"; "no atendimento de vocês nunca consigo resolver,
        pois fica voltando ao menu"
- 01/09 09:07  cliente conversa com Ume–Atendimento ao Cliente (central responde)
- 01/09 09:09  varejo posta 3 prints no grupo
- 01/09 09:14  "Alguém?????"
- 01/09 09:38  primeira resposta da Ume no grupo (**43 min após a abertura**)
- 01/09 09:56  "Não sei ele foi embora, não podia esperar" -> **cliente perdido**
- 01/09 10:25  escalado ao Slack #ask-retail-priority
- 02/09 08:40  bot diz que equipe humana está fora do horário
- 02/09 15:34  encerrado no Slack: "cliente não atendeu"
**30 dias do pagamento ao encerramento sem resolução. 2 escalações. 1 visita perdida.**

## A5. Falha de produto observada nos prints
- Biometria travada em "Solicite o escaneamento do QR Code / Verificar status da biometria"
- Ativação de licença PAYMOBI presa em "já estamos ativando sua licença..."
- POS em "Configuração ainda não confirmada. Aguarde alguns instantes e tente novamente"
  (varejo esperando >10 min; orientação da Ume foi acionar o livechat e reclamar da demora)

## A6. Frase recorrente do varejo sobre o canal oficial
- "no atendimento de vocês nunca consigo resolver, pois fica voltando ao menu"
- "No atendimento fica só mandando mensagem automática"
- "só conseguimos falar com vocês quando pede prioridade"
- "não é o primeiro cliente que paga no sábado e não dá baixa"
- "Já tem mais de meia hora que estou esperando o atendimento" (03/09)

## Pendente de leitura
64 fotos, agrupadas em ~20 casos distintos. Clusters maiores ainda não lidos:
01/09 17:30 (10 fotos, "clientes não conseguem resolver pendências"),
02/09 09:24 (11 fotos, mesmo caso do A3), 24/08 10&Cia (5, condição de venda),
29/08 Top Móveis (6, conferir venda), 04/08 Top Móveis (4, acessos nova financeira).

---

# Colheita de identificadores — 2ª rodada (14 prints lidos)

## A7. O bot responde "você não tem nenhuma compra em aberto" — e a cobrança continua

Padrão confirmado em **dois clientes distintos**, ambos no canal
**Ume – Atendimento ao Cliente** (verificado), roteiro idêntico:

1. bot: "Entendi que você já pagou, mas ainda está recebendo cobranças.
   Foi por PIX ou código de barras?"
2. bot: "se foi por código de barras, pode levar até **3 dias úteis** para compensar"
3. cliente: "código de barras"
4. bot: "**[nome], vi aqui que você não tem nenhuma compra em aberto com a Ume 😀**"

- Cliente A (CPF-9f7b325b64), 19/08 09:43 — pagamento de 03/08, 16 dias antes
- Cliente B (sem CPF visível), 01/09 16:56 — mesma sequência, mesmo dia em que
  o cliente A voltou à loja

A conversa termina ali. A cobrança automática segue disparando. São dois sistemas
da Ume dando respostas opostas sobre o mesmo contrato, no mesmo dia.

## A8. Segundo prazo oficial declarado

Além das **12 horas úteis** para solicitação do varejo (A1), o canal do cliente
declara **3 dias úteis** para compensação de pagamento por código de barras.
Nos dois casos observados o pagamento tinha 16 e 29 dias — muito fora do prazo
declarado, e ainda assim sem baixa.

## A9. A mensagem de cobrança automática tem defeito de template

Print de 15/07: "Confirmação de pagamento Crédito Sipolatti pendente
**OiMaria**, ainda não recebemos a confirmação do seu pagamento."
Saudação e nome colados. Cliente já havia pago em 06/07; a cobrança de 15/07
pedia R$ 297,95 contra os R$ 286,36 pagos — diferença de juros sobre parcela quitada.

## A10. O funil de vendas por filial circula nos grupos

Print de 06/08 (Sipolatti): tabela "Funil de vendas por ponto de venda" com
25 filiais, colunas clientes consultados / aprovados / vendas / valor financiado.
**É o denominador de normalização que falta ao projeto** — e ele já existe,
é gerado internamente e postado no grupo.

## Rendimento da colheita de CPF

14 prints lidos, **2 CPFs** colhidos, ambos de comprovante bancário.
Conversa com a central mostra só o primeiro nome; tela de erro não mostra nada.
Confirma o diagnóstico: o print serve para provar o caso, não para indexar o cliente.

---

# 3ª rodada — o canal Apoio Financeiro, acompanhado por 3 dias

Uma mesma cliente do Sipolatti, parcela de julho paga, acompanhada nos prints:

| quando | o que o canal oficial respondeu |
|---|---|
| 02/09 08:40 | "nossa **equipe humana está fora do horário de atendimento**, não consigo verificar o pagamento feito há mais de um mês" — oferece gerar boleto ou **renegociar** |
| 02/09 09:24 | "**não estou conseguindo fazer a transferência para o atendimento humano** [...] eles estarão disponíveis **amanhã, 03/09, a partir das 8h**" — oferece boleto ou **renegociação** |
| 03/09 09:41 | oferece "o boleto da parcela de setembro **com os encargos atuais**" |
| 03/09 09:42 | cliente: *"Como eu já paguei quero sem juros"* → bot: *"Vou te transferir para um atendente humano. Aguarde um momento."* |
| 03/09 09:51 | cliente: "Oi" |
| 03/09 10:02 | cliente: "Oiiiii" |
| 03/09 10:23 | **41 min sem nenhuma resposta.** Varejo recorre ao grupo: *"Já tem mais de meia hora que estou esperando o atendimento"* |

## A11. A transferência para humano falha e não avisa

Em 02/09 o bot declarou indisponibilidade de handoff **pelo dia inteiro** de um dia
útil. Em 03/09 prometeu transferir e simplesmente não transferiu — a cliente ficou
41 minutos mandando "Oi" para o vazio.

## A12. A oferta de renegociação e de juros aparece em todos os casos

Nos quatro prints do canal financeiro, a saída oferecida a quem já pagou é sempre
a mesma: **gerar novo boleto (com encargos) ou iniciar renegociação**. Nenhuma
oferece "vou verificar seu comprovante". É o roteiro, não o acaso.

## A13. Três pagamentos comprovados, nenhum baixado

| pago em | valor | dias sem baixa até a cobrança |
|---|---:|---:|
| 01/08/2026 | R$ 140,44 | 31 |
| 03/08/2026 | R$ 226,93 | 29 |
| 06/07/2026 | R$ 286,36 | 9 |

Mediana 29 dias. Todos com comprovante bancário fotografado. Todos do Sipolatti.
Os três contra um prazo de compensação **declarado pelo próprio canal de 3 dias úteis**.

## Limitação de método a partir daqui

O ambiente bloqueia gravar CPF em claro, inclusive para gerar hash — o que está
correto. **Não colho mais CPF.** Os prints com CPF ficam marcados
`cpf_visivel_no_print: true` e o hash fica `PENDENTE-extrair-localmente`.
Para fechar o cruzamento, rodar `colher.py` localmente com o mesmo salt.

---

# 4ª rodada — 33 prints lidos

## A14. O canal encerra o atendimento quando não localiza o cadastro
Print 28/08 (Novo Mundo), canal oficial:
- bot pede "CPF do titular da compra, apenas números, Ex: 10987654321"
- cliente digita o CPF **duas vezes**, no formato exato pedido
- bot: *"Desculpe mas não consegui entender o seu CPF para localizar seu cadastro! 😅"*
- bot: *"Como não conseguimos localizar seu cadastro **não podemos seguir com o atendimento**."*

Terminação por falha de identificação. O cliente não é atendido e não recebe
alternativa. É um modo de falha distinto dos anteriores.

## A15. O ping-pong do reset de senha, agora com evidência dos dois lados
Print 22/06 (Mag Duarte): tela de login do portal com
*"Usuário não cadastrado ou senha incorreta"*, vendedor com cliente em loja.
A própria tela orienta: *"Esqueceu seus dados de acesso? Fale conosco pelo
atendimento ao varejo pelo WhatsApp (11) 4020-4025"*.
É exatamente o canal que, segundo a thread do Slack de 16/06, responde que não
faz esse atendimento e manda procurar a central do cliente.
**O produto manda para um lugar que recusa o pedido.**

## A16. Biometria: três falhas distintas no mesmo fluxo
- *"Falha ao consultar biometria"* (06/08)
- travado em *"Solicite o escaneamento do QR Code / Verificar status da biometria"* (06/08)
- *"Solicitação iniciada em outro dispositivo"* ao passar do aparelho da loja
  para o do cliente (20/05)
O fluxo exige emprestar o aparelho da loja ao cliente ou ler QR Code para
continuar no celular dele — e quebra na passagem.

## A17. Entrada mínima sem explicação
Print 08/08 (Top Móveis): compra de **R$ 2.750,00**, entrada mínima oferecida de
**R$ 1.750,00** — 64% do valor. A tela lista as opções e não explica o motivo nem
oferece caminho alternativo. É o subtipo C do cluster de crédito do material
anterior, agora com número.
Nota: **o portal mascara o CPF na própria tela** (`048.***.***-38`). Os
comprovantes bancários fotografados expõem tudo.

## A18. A base da central existe com os campos certos
Print 06/08: console interno do atendimento, mostrando id do ticket,
"Contactado há poucos segundos", "Criada em", nome do agente e
*"Sistema alterou o status para Abrir 13:34"*.
Confirma que o sistema tem **ticket id, timestamps, status e agente** — os campos
pedidos para o cruzamento. O pedido é viável.

## A19. Exposição de dado de colaborador
Print 04/08 (Top Móveis): planilha `operator_name` + `operator email` com cerca de
33 operadores de loja, compartilhada como imagem num grupo de 30 participantes.
Os acessos ao portal estão atrelados a **e-mails pessoais** (gmail, hotmail, yahoo),
não corporativos — sem revogação quando o colaborador sai.
Nenhum dado reproduzido neste registro.

---

# Segunda leva: os 46 prints restantes

Com estes, os **75 prints triados** foram lidos. A numeração segue de A19.

## A20. O caso mais bem documentado do acervo: 56 dias de cobrança sobre parcela paga
Uma mesma cliente aparece em **três prints, de três datas diferentes**, e os três
se encaixam:

| Quando | O que o print mostra |
|---|---|
| 15/07 | Boleto IUGU, vencimento **04/07/2026**, **R$ 286,36** |
| 06/08 | Bot cobra **R$ 310,66**, "maior atraso **29 dias**" |
| 02/09 | Bot cobra **R$ 330,49** "com os encargos", atraso de ~2 meses |

No print de 02/09 a cliente envia o comprovante bancário, legível na tela:
**pago em 08/07/2026**, mora/multa R$ 0,00, autenticação digital.
Pagou quatro dias após o vencimento e seguiu sendo cobrada por 56 dias.
O valor exigido subiu **R$ 286,36 → R$ 330,49 (+15,4%)**.

Observado. A leitura de que a diferença é encargo sobre parcela já quitada é
interpretação — mas o próprio bot a confirma em texto: *"os encargos (juros e
multa) são calculados automaticamente sobre as parcelas em atraso"*.

## A21. O fluxo de cobrança não tem opção para "já paguei"
Print 01/09: bot cobra R$ 254,04 / 16 dias e oferece dois botões —
*2ª via Boleto* e *Menu inicial*. O cliente escreve **"Eu ja paguei"**.
Resposta: *"Ops! Não consegui entender sua resposta. 😬 Para continuar, você
precisa escolher uma das opções acima."*

Não é lentidão nem fila. **A contestação não existe como caminho no menu.**

## A22. A única saída oferecida a quem já pagou é renegociar
Sequência de 02/09, 08:44–08:46, sempre a mesma cliente:
- *"não consigo gerar um boleto sem esses valores"* (sem os encargos)
- *"o que posso te oferecer é iniciar um fluxo de renegociação"*
- cliente: *"Não tem renegociação, eu já paguei"*
- bot: *"O sistema ainda me mostra a parcela de julho como em aberto"*

As duas ações que o canal consegue executar sozinho — **gerar boleto e
renegociar** — são as duas que aumentam a dívida. A ação que resolveria —
dar baixa no pagamento — depende de humano.

## A23. A reclamação de cobrança indevida é encerrada como "feedback"
Mesma conversa, 08:46:
*"Gostaria de registrar sua reclamação sobre o pagamento não reconhecido?
Assim, nossa equipe terá o registro quando voltar ao expediente."* → *"Com
certeza"* → **"Feedback registrado com sucesso."**

Sem número de protocolo, sem prazo, sem suspensão da cobrança. Uma contestação
de cobrança vira um registro de satisfação.

## A24. A prova é entregue num canal que declara não saber lê-la
Às 08:47 a cliente envia boleto e comprovante. O bot responde
*"Obrigado por enviar o comprovante, Maria! Está registrado"* — e na mesma
mensagem repete que *"a verificação de pagamentos mais antigos que não foram
processados em nosso sistema precisa ser feita pela equipe de atendimento
humano, que está offline agora."*

O documento entra no canal e para ali.

## A25. Três horários de atendimento diferentes na mesma conversa
Tudo em 02/09, entre 08:40 e 08:48, do mesmo bot:
1. *"Atendimento: Seg a Sáb 9h às 23h, Dom 10h às 19h20"*
2. *"Você pode tentar novamente amanhã, das 8h às 18h"*
3. *"trabalha de segunda a sexta-feira, das 8h às 18h. Hoje, 02/09/2026, sendo
   uma quarta-feira, eles já encerraram o expediente"* — **dito às 08:48 da manhã**

Quando a cliente contesta (*"Como assim é 8:48 da manhã"*), o bot admite:
*"Você está absolutamente certa. Minha informação estava incorreta."*, oferece
transferir para um atendente, a cliente responde **"Sim"** — e a resposta
seguinte é de novo *"Nosso time de atendimento está fora…"*.

**O loop se fecha sobre si mesmo.** É a documentação mais limpa que temos da
pergunta "o cliente consegue chegar numa pessoa?". Nove minutos de negativa
baseada em informação errada, correção, oferta, aceite — e volta ao início.

## A26. O canal cobra e, 35 minutos depois, diz que não há compra
Mesmo CPF, mesmo canal, mesmo dia (01/09):
- **09:08** — *"1 parcela(s) vencida(s)", "maior atraso 16 dias", "R$ 254,04"*
- **09:43** — *"vi aqui que você não tem nenhuma compra em aberto com a Ume 😀"*

Um segundo cliente, no mesmo lote de prints, recebe a mesma frase depois de
dizer *"No app ainda consta o débito"*. Ambos têm comprovante bancário pago em
03/08 (R$ 226,93 e R$ 140,44).

## A27. O app conta zero parcelas pagas
Print do app, aba **"Minhas parcelas"**: *Pendentes 9* / **Pagas 0** — de um
cliente que tem comprovante bancário autenticado.

Na mesma tela, o preço riscado aparece em três linhas:
`04 AGO R$ 153,62 ~R$ 141,91~ (Atrasada)`, `04 SET R$ 134,70 ~R$ 141,91~`,
`04 OUT R$ 121,36 ~R$ 141,91~`. **O mesmo padrão visual de preço riscado serve
para desconto de antecipação e para acréscimo de encargos.**

## A28. O portal tem comprovante — só que ele some
Sequência de 29/08 numa loja Top Móveis, com hora de cada print:

| Hora | Tela |
|---|---|
| 09:33 | "Configuração de Loja" — selecionar a filial |
| 09:38 | Home do portal: **só** Super Compra, Configurações, Sair |
| 09:44 | Canal de atendimento ao varejo, digitando CPF |
| 09:45 | Bot devolve contrato e link de comprovante |

E o print de 19/08 mostra por quê: a tela **"Venda concluída"** oferece
*Acessar CCB*, *Visualizar comprovante*, *Gerar próximo*. Essas ações existem —
**mas só naquela tela**. Depois que o vendedor fecha, não há caminho de volta
pela home. Sete minutos e um acionamento de canal para recuperar algo que o
produto já emitiu.

## A29. A Ume é a 5ª de seis na lista escrita à mão
Em três lojas diferentes, os prints capturam o mesmo cenário sem querer:
- Post-it colado no monitor: *Credipar, Kerocredito, Afins, Crefaz, **UME**, DM*
- Barra de favoritos com Crefaz, CREDZ, Credipar.NET, OmniFácil, Pitzi,
  FortBrasil, Boleto Simples, Kerocredito, Auditor Caixa
- Abas abertas ao lado do portal da Ume: BrasilCard, Credipar, Ucred,
  FortBrasil lojista

Isso dá peso comercial ao próximo achado.

## A30. "Crédito não aprovado" com um único botão: Encerrar consulta
Print 04/08: *"O carrinho criado não pôde ser aprovado nesse momento."*
Sem motivo, sem valor alternativo, sem contraproposta, sem recurso. A única
ação é **Encerrar consulta**.

Com A29 ao lado, o custo é direto: a recusa seca devolve o vendedor para as
abas da concorrência, que estão abertas na mesma janela.

## A31. O canal encerra o atendimento e culpa o cliente pelo CPF
Print Novo Mundo, 21/08, 09:51–09:52. O cliente digita o CPF **duas vezes**,
11 dígitos, só números, exatamente como o exemplo do próprio bot.
- *"Desculpe mas não consegui entender o seu CPF para localizar seu cadastro! 😅"*
- *"Como não conseguimos localizar seu cadastro **não podemos seguir com o
  atendimento**. Estou encerrando nossa conversa. 😌"*
- reinício → cliente escreve "Oi" → *"Por favor, respeite a quantidade certa de
  caracteres do CPF incluindo se houver 0 no início…"*

O canal termina o atendimento e atribui a falha ao formato digitado pelo cliente.

## A32. Credencial entregue em texto aberto — e depois refotografada
Print 03/08: o canal oficial *Ume - Atendimento ao Varejo*, rolado até
**dez/2025**, com *"Bem-vindo! Seu acesso à Ume está pronto! Login: … Senha: …"*
seguido de *"Dica de segurança: Não compartilhe suas credenciais com terceiros."*
A mensagem que entrega a senha é a mesma que pede para não compartilhá-la — e
acabou de ser fotografada e postada num grupo de 30 pessoas.

No mesmo enquadramento: **post-its com login e senha escritos à mão, colados no
teclado da loja**.

Um segundo print (04/08, outra rede) mostra a via de e-mail: mensagem de uma
conta **pessoal** (@hotmail) para a loja, *"Segue abaixo o acesso da nova
financeira UME"* — e no lugar do acesso, *"A imagem vinculada não pode ser
exibida"*. A credencial ia embutida como imagem e não carregou.

Junto com A15 (o portal manda para o canal que recusa reset de senha) e A19
(planilha de 33 operadores com e-mail pessoal), fecha-se o ciclo: **não existe
um caminho próprio e seguro de entrega e recuperação de acesso.**

## A33. O cupom coloca compra e contrato lado a lado
Print 28/08 (Magazine Duarte), cupom "via caixa":
`Valor da Compra R$ 1.190,82` / `Valor do Contrato R$ 2.582,80` — 12 × R$ 215,23.
Dado observado, sem juízo aqui: é a informação que o cliente leva para casa e a
base concreta de boa parte das contestações posteriores.

## A34. O que o material de venda promete
Card co-marcado Ume + varejo (03/09) publica os canais e as promessas:
- Central do Cliente **(11) 4020-1960** · Central do Vendedor **(11) 4020-4025**
- LiveChat: *"fale diretamente com um especialista"*
- *"Nosso cadastro leva ~02 MIN"*, *"Liberação é Imediata"*, *"até 14x"*,
  **"Desconto para Pagamentos Antecipados"**

Duas leituras:
1. O mesmo número 4020-4025 aparece como "Central do Vendedor" e como "Central
   de Atendimento Ume" no rodapé — o varejo e a dúvida geral caem no mesmo lugar.
2. **"Desconto para pagamentos antecipados"** é exatamente o argumento que a
   cliente de A20 usa ao contestar: *"não aceito pagar juros de uma parcela que
   eu já paguei e paguei antecipado"*. A promessa da vitrine e o comportamento
   da régua de cobrança se contradizem.

## A35. Funil de aprovação, dado observado
Os painéis que a Ume posta nos grupos trazem número próprio de aprovação:

| Rede / data | Consultados | Aprovados | Vendas |
|---|---|---|---|
| Sipolatti 06/08 | 136 (1 filial) | 46 | 16 |
| Mag Duarte 07/08 | 62 | 13 (21%) | 5 |
| Mag Duarte 06/08 | 10 | 2 | 1 |
| Top Móveis 07/08 | 36 | 5 (14%) | — |

Não é dado de suporte, mas dimensiona o cluster de crédito: **a maioria das
consultas não vira aprovação**, e A30 mostra que a recusa sai sem explicação.

Observação operacional de brinde: o painel do Top Móveis lista
*"ACARAÚ - LOJA INATIVA"* com **5 clientes consultados**. Loja marcada como
inativa segue consultando.

## A36. Outros pontos de handoff no meio da venda
- **Unico** (30/08): *"Verifique sua identidade com a Unico"*, R$ 1.905,00 em
  10×. A URL carrega `forcaRetryPopup=1` — o fluxo já havia falhado antes.
- **Biometria** (06/08, dois prints): *"Falha ao consultar biometria"* e a tela
  de QR Code travada em *"Verificar status da biometria"*. Confirma A16.
- **PIX Parcelado** (02/09): *"não está disponível para a sua conta no momento"*,
  sem alternativa.

## Nota de método
A regra de PII segue valendo: **nenhum CPF foi coletado em texto aberto**.
Prints com CPF visível estão marcados `cpf_visivel_no_print: true` e
`cpf_id: "PENDENTE-extrair-localmente"`, para serem hasheados na máquina da
Luana com `colher.py` e o mesmo salt. Valores, datas, IDs de contrato e falas
do bot são reproduzidos porque são o que sustenta o achado.
