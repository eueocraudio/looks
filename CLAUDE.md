# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

**looks** — aplicação desktop para gerenciamento de sistemas de arquivos LUKS (Linux Unified Key Setup).

## Executar

```bash
python3 src/main.py
```

## Stack

- **Linguagem:** Python 3
- **Interface gráfica:** PySide6

## Estrutura

```
src/        # todo o código Python
  main.py   # ponto de entrada, janela principal (MainWindow)
```

## Arquitetura

- `MainWindow` (`src/main.py`) — janela principal com dimensão fixa 850×450. Contém a barra de menus com três entradas: **File** (Open, Create, Close), **Partition** (Resize, Change Secret, Close) e **About**.
- O encerramento do app passa por `_close_app`, que fecha a janela, executa `gc.collect()` e chama `QApplication.quit()`.
