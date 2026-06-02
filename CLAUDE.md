# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

**looks 1.0.0** — aplicação desktop para gerenciamento de sistemas de arquivos LUKS (Linux Unified Key Setup). Deve ser executada como superusuário (`sudo`).

## Executar

```bash
sudo python3 src/main.py
```

## Instalar dependências

```bash
bash install.sh
```

## Stack

- **Linguagem:** Python 3
- **Interface gráfica:** PySide6
- **Dependências Python:** `python-dotenv`
- **Dependências do sistema:** `cryptsetup`, `cryptsetup-bin`

## Estrutura

```
src/            # todo o código Python
  main.py       # ponto de entrada, janela principal (MainWindow)
  open.py       # diálogo para abrir um volume LUKS existente (.img)
  create.py     # diálogo para criar um novo volume LUKS
bash/           # scripts shell
  create.sh     # cria e monta volume LUKS (cryptsetup luksFormat + open + mkfs)
  close.sh      # desmonta e fecha volume LUKS (umount + cryptsetup luksClose)
```

## Arquitetura

- `MainWindow` (`src/main.py`) — janela principal 850×450, requer root (`os.getuid() == 0`). Menus: **File** (Open, Create, Close), **Partition** (Resize, Change Secret, Close), **About**. Botão central **PANIC** (vermelho, circular) e botões inferiores **Open Application** / **Close Application**.
- `OpenWindow` (`src/open.py`) — `QDialog` modal para selecionar um `.img` existente via `QFileDialog` com arquivos ocultos visíveis. Retorna `result_path = /tmp/{name}` se o diretório estiver montado.
- `CreateWindow` (`src/create.py`) — `QDialog` modal com campo `Name:` (somente letras). Retorna `result_path = /tmp/{name}` se o diretório estiver montado.
- Ambos os diálogos exibem o comando shell equivalente em tempo real na caixa "Execute no shell:".
- O processo filho é lançado via `runuser` (como usuário comum, não root) com `start_new_session=True`. O PANIC mata o grupo de processos inteiro (`os.killpg` + `SIGKILL`) e executa `close.sh` em loop de 5 tentativas.

## Variáveis de ambiente (`.env`)

| Variável | Default | Descrição |
|---|---|---|
| `APPLICATION_PATH` | `./application/run.py` | Caminho para o script da aplicação filha |
