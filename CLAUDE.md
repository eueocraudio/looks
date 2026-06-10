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
- **Dependências Python:** `PySide6`, `python-dotenv` (ver `requirements.txt`)
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
- **Importante — execução manual:** os diálogos **não** rodam `cryptsetup`/`mount` sozinhos. Eles exibem o comando equivalente na caixa "Execute no shell:" e o usuário deve copiá-lo e executá-lo no terminal. O `Continue` apenas valida que `/tmp/{name}` já está montado (`Path.is_mount()`) antes de prosseguir; se não estiver, mostra aviso e bloqueia.
- O processo filho é lançado via `runuser -u $SUDO_USER` (como usuário comum, não root) com `start_new_session=True` — requer que `SUDO_USER` esteja definido e diferente de `root`. O PANIC mata o grupo de processos inteiro (`os.killpg` + `SIGKILL`), executa `close.sh` em loop de até 5 tentativas e remove o diretório de montagem.

## Convenções de código

- O código Python deste projeto usa ponto-e-vírgula (`;`) ao final de **todas** as instruções. Mantenha essa convenção ao editar.

## Localização de arquivos em runtime

- **Imagens LUKS:** `create.sh` grava o `.img` em `/home/$SUDO_USER/{name}.img`.
- **Ponto de montagem:** sempre `/tmp/{name}` (em `bash/` e nos diálogos).
- **Argumentos de `close.sh`:** `$1` = caminho de montagem, `$2` = nome do mapper (`/dev/mapper/{name}`).

## Variáveis de ambiente (`.env`)

| Variável | Default | Descrição |
|---|---|---|
| `APPLICATION_PATH` | `./application/run.py` | Caminho para o script da aplicação filha |
