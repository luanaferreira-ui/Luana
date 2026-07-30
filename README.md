# Painel de Demandas

Ferramenta local para acompanhar e dar baixa nas demandas de trabalho. O
`demandas.json` é a **fonte de verdade** e mora no disco; um servidor mínimo em
Node (`node:http`, **zero dependências**) serve o painel e grava cada alteração
com escrita atômica + backup.

## Rodar

```bash
npm start
```

Depois abra **http://localhost:4321**. Só isso — não há build nem `npm install`.

## Como funciona

- **Fonte de verdade:** `demandas.json`. Toda mutação (marcar feito, editar prazo,
  importar, criar, remover) é gravada na hora:
  1. o arquivo atual é copiado para `.backup/demandas-<timestamp>.json` (mantém os 20 mais recentes);
  2. o novo conteúdo é escrito num `.tmp` e renomeado por cima (rename atômico).
  Se o processo cair no meio, o disco nunca fica quebrado.
- **Período (`corte`):** `demandas.json` tem `"corte": "2026-07-01"`. Nada com prazo
  anterior a essa data entra por criação ou importação. Para virar o mês, edite só
  esse campo no JSON.
- **Clusters:** os 7 vêm do próprio JSON (natureza da demanda). `conta` é a tag
  transversal — você fatia pelos dois eixos sem duplicar item.

## API (localhost only, 127.0.0.1)

| Método | Rota | O quê |
|---|---|---|
| GET | `/api/state` | estado inteiro (`corte`, `clusters`, `demandas`) |
| PATCH | `/api/demanda/:id` | atualiza `status` / `prazo` / `titulo` / `cluster` (também `conta`, `responsavel`, `urgente`) |
| POST | `/api/demanda` | cria |
| DELETE | `/api/demanda/:id` | remove |
| POST | `/api/importar` | importa um bloco de texto (`{ "texto": "..." }`) |

Toda mutação responde com a lista completa atualizada, então o front nunca
diverge do disco.

## Importar em massa

Botão **Importar**. Uma demanda por linha, tolerando prefixo `- [ ]`:

```
cluster | conta | responsável | AAAA-MM-DD | descrição
```

A data pode ficar vazia (fica sem prazo). Deduplica pelo título normalizado
(minúsculas, sem acento, sem pontuação) e **nunca mexe no status de quem já
existe**. Ao final informa: quantas entraram, quantas eram repetidas, quantas
ficaram fora do período e quantas linhas foram ignoradas por formato. É esse o
formato que o radar do Granola cospe na sua DM — dá para colar direto aqui.

## Subir automaticamente ao ligar o computador

Escolha o seu sistema:

### macOS (launchd)

Crie `~/Library/LaunchAgents/com.luana.painel-demandas.plist` (ajuste os dois
caminhos em maiúsculo):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.luana.painel-demandas</string>
  <key>ProgramArguments</key>
  <array>
    <string>/CAMINHO/PARA/node</string>
    <string>/CAMINHO/PARA/painel-demandas/server.js</string>
  </array>
  <key>WorkingDirectory</key><string>/CAMINHO/PARA/painel-demandas</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
```

Descubra o caminho do node com `which node`. Depois:

```bash
launchctl load ~/Library/LaunchAgents/com.luana.painel-demandas.plist
```

Pronto — sobe no login e reinicia sozinho se cair. Para parar:
`launchctl unload ~/Library/LaunchAgents/com.luana.painel-demandas.plist`.

### Windows

Abra o **Agendador de Tarefas** → *Criar Tarefa* → disparador *Ao fazer logon* →
ação *Iniciar programa*: `node` com argumento `server.js` e "Iniciar em" apontando
para a pasta do projeto. Marque "Executar estando o usuário conectado".

### Linux (systemd --user)

Crie `~/.config/systemd/user/painel-demandas.service`:

```ini
[Unit]
Description=Painel de Demandas
[Service]
WorkingDirectory=/CAMINHO/PARA/painel-demandas
ExecStart=/usr/bin/node server.js
Restart=always
[Install]
WantedBy=default.target
```

E rode `systemctl --user enable --now painel-demandas`.

> Depois de configurar, é só deixar aberto **http://localhost:4321** fixado no
> navegador. O servidor já está de pé quando você liga a máquina.
