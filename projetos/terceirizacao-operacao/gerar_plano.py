# -*- coding: utf-8 -*-
"""Fonte única do plano. Roda `python3 gerar_plano.py` para regerar plano.json,
o tracker .xlsx e as linhas do Painel de Demandas."""
import json, datetime

FASES = [
 dict(id="F1", nome="Enquadramento", dono="Luana", apoio="Luiza",
      inicio="2026-08-26", fim="2026-09-04",
      objetivo="Fechar escopo, métricas e cadência antes de aprofundar qualquer coisa.",
      entregavel="One-pager de escopo + régua de segmentação + tracker no ar",
      saida="Escopo escrito e aprovado pelo Lucas; 4 métricas com baseline; tracker populado e cadência na agenda.",
      depende="—"),
 dict(id="F2", nome="Descoberta e escolha do modelo", dono="Luana", apoio="Luiza",
      inicio="2026-09-08", fim="2026-09-30",
      objetivo="Saber o que o mercado faz e o que o jurídico proíbe, e escolher UM modelo — sem ainda desenhar remuneração.",
      entregavel="Comparativo de modelos com recomendação + direcional jurídico mínimo + baseline de CAC",
      saida="Um modelo escolhido e defendido ao Lucas, com os red flags jurídicos conhecidos e o inventário da operação levantado.",
      depende="F1"),
 dict(id="F3", nome="Desenho do modelo", dono="Luana", apoio="Luiza",
      inicio="2026-10-01", fim="2026-11-13",
      objetivo="Transformar o modelo escolhido em remuneração, business case, contrato e playbook.",
      entregavel="Cenário de remuneração escolhido + business case + minuta de contrato + guias e specs de dash",
      saida="Remuneração escolhida entre 3 cenários, business case aprovado pelo Financeiro, parecer do Thiago e minuta de contrato pronta.",
      depende="F2"),
 dict(id="F4", nome="Prontidão operacional", dono="Luiza", apoio="Luana",
      inicio="2026-11-16", fim="2026-12-18",
      objetivo="Contratar o parceiro e deixar a operação pronta para ir a campo.",
      entregavel="Contrato assinado, dashboards no ar, guias publicados e representante certificado",
      saida="Checklist de go/no-go assinado: contrato válido, ciclo de pagamento testado, dash no ar, carteira transferida.",
      depende="F3"),
 dict(id="F5", nome="Piloto assistido e decisão", dono="Luiza", apoio="Luana",
      inicio="2027-01-11", fim="2027-04-08",
      objetivo="Rodar a carteira-piloto, apurar três ciclos e decidir escalar, ajustar ou encerrar.",
      entregavel="Piloto em campo + 3 apurações + recomendação formal ao Lucas",
      saida="Recomendação entregue com leitura das hipóteses e do business case real contra o modelado.",
      depende="F4"),
]

# id, fase, título, dono, esforço(h), data alvo, dependência, prioridade, áreas
T = [
 # F1
 ("T1.1","F1","Escrever o one-pager de escopo: objetivo, dentro, fora e definição de pronto","Luana",3,"2026-08-28","—","P0","—"),
 ("T1.2","F1","Fechar as 4 métricas de sucesso com baseline atual e meta","Luana",3,"2026-09-02","T1.1","P0","Dados"),
 ("T1.3","F1","Régua de segmentação do long tail: critério objetivo de qual varejo entra","Luiza",4,"2026-09-02","—","P0","Comercial, Dados"),
 ("T1.4","F1","Assumir o tracker: revisar tarefas, esforços e datas e travar as quatro views","Luana",2,"2026-08-31","—","P0","—"),
 ("T1.5","F1","Importar as tarefas da quinzena no Painel de Demandas e travar o ritual de baixa","Luiza",1,"2026-08-31","—","P0","—"),
 ("T1.6","F1","Criar os convites da cadência: touchpoint ter/qui, bloco de sexta, status quinzenal e comitê mensal","Luiza",1,"2026-08-27","—","P0","—"),
 ("T1.7","F1","Escrever as hipóteses que o piloto precisa testar","Luana",2,"2026-09-03","T1.2","P1","—"),
 ("T1.8","F1","Mapa de stakeholders: um ponto focal em Jurídico, Financeiro, People/DP, CS, Dados e MKT","Luiza",3,"2026-09-04","—","P1","Todas"),
 ("T1.9","F1","Apresentar o enquadramento ao Lucas e fechar o escopo","Luana",2,"2026-09-04","T1.1,T1.2","P0","Liderança"),
 # F2 — Luana
 ("T2.1","F2","Revisar a transcrição Amanda/Júlia x Thiago e extrair o direcional jurídico mínimo","Luana",4,"2026-09-11","—","P0","Jurídico"),
 ("T2.2","F2","Lista de red flags e perguntas para o Thiago: o que pode remunerar por modelo, vínculo, exclusividade, uso de marca","Luana",2,"2026-09-15","T2.1","P0","Jurídico"),
 ("T2.3","F2","Sessão de 45 min com o Thiago para o direcional (não é o parecer formal)","Luana",2,"2026-09-18","T2.2","P0","Jurídico"),
 ("T2.4","F2","Ficha do modelo de representação comercial (DTX/Imperium): remuneração, territorialidade, sub-regionais, prazo de revisão","Luana",5,"2026-09-16","—","P0","—"),
 ("T2.5","F2","Ficha dos modelos alternativos: agência de promotor (orçamento-referência) e franquia (obrigação por região)","Luana",4,"2026-09-18","—","P1","—"),
 ("T2.6","F2","Duas conversas de referência: Jérico/Imperium e um franqueado Stone regional","Luana",3,"2026-09-22","T2.4","P1","—"),
 ("T2.7","F2","Baseline de aquisição: R$14/novo cliente, 1-2% de incentivo sobre originação e o CAC real do projeto da Mandinha","Luiza",4,"2026-09-23","—","P0","Financeiro, Dados"),
 ("T2.8","F2","Comparativo pró x contra com a recomendação de modelo e defesa ao Lucas","Luana",4,"2026-09-30","T2.3,T2.4,T2.5,T2.7","P0","Liderança"),
 # F2 — Luiza
 ("T2.9","F2","Inventário do onboarding do representante: tudo que ele precisa saber para representar a UME","Luiza",5,"2026-09-18","—","P0","—"),
 ("T2.10","F2","Inventário do onboarding do varejo, no modelo do que foi feito com o Habit","Luiza",4,"2026-09-22","—","P0","Comercial"),
 ("T2.11","F2","Mapear com o time da Amanda o fluxo de cadastro de lojas/operadores e a distribuição de acessos","Luiza",4,"2026-09-23","—","P0","Comercial, Tech"),
 ("T2.12","F2","Gap de dados: o que o Looker já entrega contra o que o dash self-service precisa","Luiza",4,"2026-09-25","—","P1","Dados"),
 ("T2.13","F3","Mapa de exceções: o que o atendimento resolve e o que sobra para o time interno","Luiza",3,"2026-10-09","—","P1","CS"),
 ("T2.14","F3","Levantar o que existe hoje de peça de trade e de brand book","Luiza",2,"2026-10-16","—","P2","MKT"),
 # F3 — Luana
 ("T3.1","F3","Árvore de métricas: CAC como âncora, componente de recorrência e guardrails de FPD, MOIC e inadimplência","Luana",5,"2026-10-09","T2.7,T2.8","P0","Financeiro, Risco"),
 ("T3.2","F3","Modelar os 3 cenários de remuneração: 100% variável em CAC; CAC + recorrência; fixo + variável com gatilho","Luana",8,"2026-10-20","T3.1","P0","Financeiro"),
 ("T3.3","F3","Business case: ponto de equilíbrio por carteira e custo de incentivo contra originação","Luana",6,"2026-10-27","T3.2","P0","Financeiro"),
 ("T3.4","F3","Regras de apuração e pagamento (parte em 30 dias, parte condicionada) e emissão de NF","Luana",4,"2026-10-30","T3.2","P0","Financeiro, DP"),
 ("T3.5","F3","Matriz de alçadas: o que o representante negocia (limite, juros, MDR) e o que a UME nunca terceiriza","Luana",4,"2026-10-23","T2.1","P0","Risco, Crédito"),
 ("T3.6","F3","Parecer do Thiago sobre o cenário escolhido","Luana",3,"2026-11-06","T3.3,T3.5","P0","Jurídico"),
 ("T3.7","F3","Minuta de contrato: prazos, métricas, custos, responsabilidades, territorialidade, LGPD e rescisão","Luana",6,"2026-11-13","T3.6","P0","Jurídico"),
 ("T3.8","F3","Perfil e critérios de seleção do representante, com People","Luana",4,"2026-11-06","—","P1","People"),
 ("T3.9","F3","Estrutura hierárquica: quem é o dono do modelo na UME e por qual canal o representante fala com a gente","Luana",3,"2026-10-30","—","P1","People"),
 # F3 — Luiza
 ("T3.10","F3","Trilha de onboarding do representante: conteúdo, roteiro e certificação de aptidão","Luiza",8,"2026-10-23","T2.9","P0","—"),
 ("T3.11","F3","Guia 'o que fazer com o varejo': ativação passo a passo, treinamento operacional e financeiro","Luiza",8,"2026-10-30","T2.10","P0","CS"),
 ("T3.12","F3","Spec do dash de operação self-service: consulta, venda, aprovação, conversão, filtros e export CSV","Luiza",5,"2026-10-16","T2.12","P0","Dados"),
 ("T3.13","F3","Spec do dash financeiro e do CSV que sustenta a apuração da remuneração","Luiza",4,"2026-10-23","T3.1","P0","Dados, Financeiro"),
 ("T3.14","F3","'DP do representante': NF, prazo e forma de pagamento, canal oficial e acessos","Luiza",4,"2026-11-06","T3.4","P1","DP, Tech"),
 ("T3.15","F3","Fluxo alvo de cadastro e acessos + SLA com o time da Amanda","Luiza",5,"2026-11-06","T2.11","P1","Comercial, Tech"),
 ("T3.16","F3","Guia de boas práticas (uniformização, promotor de loja) escrito como recomendação, nunca obrigação","Luiza",3,"2026-11-13","—","P1","Jurídico, MKT"),
 ("T3.17","F3","FAQ e canais de atendimento do varejo","Luiza",4,"2026-11-13","T3.11","P2","CS"),
 ("T3.18","F3","Rotina de ongoing do representante: report, apuração, agenda de alinhamento e fluxo de exceção","Luiza",4,"2026-11-13","T2.13","P1","CS"),
 # F4
 ("T4.1","F4","Definir a carteira do piloto aplicando a régua de segmentação","Luana",4,"2026-11-20","T1.3","P0","Comercial, Dados"),
 ("T4.2","F4","Prospectar e selecionar o parceiro do piloto, avaliando usar a estrutura que já roda como piloto zero","Luana",10,"2026-12-04","T3.8","P0","People"),
 ("T4.3","F4","Negociar e assinar o contrato do piloto","Luana",6,"2026-12-11","T3.7,T4.2","P0","Jurídico, Financeiro"),
 ("T4.4","F4","Cadastrar o parceiro como fornecedor e testar o ciclo apuração > NF > pagamento","Luana",4,"2026-12-18","T4.3","P0","Financeiro, DP"),
 ("T4.5","F4","Status de fechamento do ano para o Lucas","Luana",2,"2026-12-18","—","P1","Liderança"),
 ("T4.6","F4","Publicar o dash de operação e o dash financeiro com a carteira-piloto carregada","Luiza",8,"2026-12-04","T3.12,T3.13,T4.1","P0","Dados"),
 ("T4.7","F4","Publicar o repositório de peças de trade e o recorte de brand book, com dono e SLA de atualização","Luiza",5,"2026-11-27","T2.14","P0","MKT"),
 ("T4.8","F4","Publicar os guias, o FAQ e os canais de atendimento","Luiza",4,"2026-12-04","T3.11,T3.17","P0","CS, MKT"),
 ("T4.9","F4","Rodar o onboarding e certificar o representante do piloto","Luiza",8,"2026-12-18","T3.10,T4.3","P0","—"),
 ("T4.10","F4","Passar a carteira: lojas cadastradas, operadores e acessos na mão do representante","Luiza",4,"2026-12-18","T3.15,T4.1","P0","Comercial"),
 ("T4.11","F4","Rodar o checklist de go/no-go do piloto","Luiza",2,"2026-12-18","T4.4,T4.6,T4.8,T4.9,T4.10","P0","—"),
 # F5
 ("T5.1","F5","Go-live e operação assistida, com diário de bordo semanal","Luiza",36,"2027-03-31","T4.11","P0","—"),
 ("T5.2","F5","Apuração mensal da remuneração (fev, mar e abr)","Luana",12,"2027-04-05","T4.4","P0","Financeiro"),
 ("T5.3","F5","Medir as hipóteses: tempo liberado do time interno, originação incremental e qualidade da carteira","Luana",8,"2027-03-31","T1.7","P0","Dados"),
 ("T5.4","F5","Retrospectiva por ciclo e ajuste do playbook","Luiza",9,"2027-03-31","T5.1","P1","—"),
 ("T5.5","F5","Refresh de treinamento a cada atualização operacional, do representante ao varejo","Luiza",6,"2027-03-31","T4.9","P1","—"),
 ("T5.6","F5","Escrever a recomendação de escalar, ajustar ou encerrar e levar ao Lucas","Luana",6,"2027-04-08","T5.2,T5.3,T5.4","P0","Liderança"),
]

METRICAS = [
 ("M1","Horas/semana do time interno gastas com varejo long tail","A medir na F1 (amostra de 2 semanas)","-60% até o fim do piloto","Luana","Apontamento das duas + agenda"),
 ("M2","Varejos ativos sob carteira terceirizada","0","10 a 15 lojas no piloto","Luiza","Dash de operação"),
 ("M3","CAC do canal terceirizado (R$ por novo cliente)","R$ 14 (referência da central de vendas)","Menor ou igual a R$ 14, com teto de 2% sobre originação","Luana","Apuração mensal"),
 ("M4","FPD e inadimplência da carteira terceirizada","A medir (média UME por região)","Até 1 p.p. acima da média UME","Luana","Risco / BigQuery"),
 ("M5","Originação da carteira-piloto contra o mesmo período do ano anterior","A medir na F4","+15% no 3º ciclo","Luiza","Dash financeiro"),
]

RISCOS = [
 ("R1","Remuneração mal calibrada: pagar sobre originação total estoura o CAC e o modelo deixa de se pagar","Alta","Alto",
  "No 1º cenário modelado, o custo por novo cliente passa de R$ 14 sem contrapartida de volume",
  "Ancorar em CAC/novos clientes com guardrails de FPD e MOIC, teto por carteira e cláusula de revisão a cada 6 meses","Luana"),
 ("R2","Uma restrição jurídica invalida o modelo depois de desenhado","Média","Alto",
  "O direcional do Thiago (T2.3) vem com 'depende' em vez de 'pode/não pode'",
  "Direcional mínimo na F2, antes de modelar remuneração; três cenários levados ao parecer em vez de um","Luana"),
 ("R3","Escopo infla: querer resolver engajamento, prospecção de varejo e comercial no mesmo pacote","Alta","Alto",
  "Aparece tarefa de rebate ou MDR no tracker sem decisão do Gate 2",
  "Lista de fora de escopo assinada na F1; prospecção só entra se a Q1 for decidida como sim, e mesmo assim fora do piloto","Luana"),
 ("R4","As 8h/semana não se sustentam quando a operação do dia a dia aperta","Alta","Alto",
  "Duas semanas seguidas com menos de 5h apontadas, ou touchpoint desmarcado 2x",
  "Bloco de sexta protegido na agenda; se a semana cair abaixo de 5h, corta-se P2 antes de empurrar P0; capacidade revista no status quinzenal","Luiza"),
 ("R5","Cadastro e acessos presos no time da Amanda viram o gargalo da operação terceirizada","Média","Médio",
  "Qualquer pedido de acesso do piloto levando mais de 48h",
  "SLA escrito na T3.15, com fila visível; automação vira backlog priorizado de Tech antes da onda 2","Luiza"),
]

def main():
    plano = dict(
      versao=2, projeto="Modelo de Terceirização da Operação",
      atualizado_em="2026-08-26",
      origem="Reunião 'Escalabilidade time' (Luiza Falcone e Luana Ferreira, 26/ago/2026) + foto do quadro",
      patrocinador="Lucas", capacidade_semanal_h=8,
      fases=FASES,
      tarefas=[dict(id=i[0], fase=i[1], titulo=i[2], dono=i[3], esforco_h=i[4],
                    data_alvo=i[5], dependencia=i[6], prioridade=i[7], areas=i[8],
                    status="Não iniciado") for i in T],
      metricas=[dict(id=m[0], metrica=m[1], baseline=m[2], meta=m[3], dono=m[4], fonte=m[5]) for m in METRICAS],
      riscos=[dict(id=r[0], risco=r[1], probabilidade=r[2], impacto=r[3], sinal=r[4], mitigacao=r[5], dono=r[6]) for r in RISCOS],
    )
    json.dump(plano, open("plano.json","w"), ensure_ascii=False, indent=2)
    return plano

if __name__ == "__main__":
    p = main()
    print("fases:", len(p["fases"]), "| tarefas:", len(p["tarefas"]))
    for d in ("Luana","Luiza"):
        print(d, sum(t["esforco_h"] for t in p["tarefas"] if t["dono"]==d), "h")
