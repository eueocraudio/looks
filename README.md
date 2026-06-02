# looks 1.0.0

Gerenciador de sistemas de arquivos LUKS (Linux Unified Key Setup) com interface gráfica. Requer execução como superusuário.

## Stack

- Python 3
- PySide6
- cryptsetup

## Instalação

```bash
bash install.sh
```

## Configuração

Edite o arquivo `.env` na raiz do projeto:

```env
APPLICATION_PATH=./application/run.py
```

## Executar

```bash
sudo python3 src/main.py
```
