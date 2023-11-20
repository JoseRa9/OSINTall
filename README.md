# OSINTall

## Usage

```bash
usage: osintall.py [-h] --mails MAILS --config CONFIG --commands COMMANDS [COMMANDS ...] [-c] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  --mails MAILS         File to read mails from
  --config CONFIG       Config file to use
  --commands COMMANDS [COMMANDS ...]
                        Commands to execute
  -c, --clean           Clean output directory
  -o OUTPUT, --output OUTPUT
                        Output directory
```

## How to add commands

In a .yml file, add a new entry as shown in example.yml

```yaml
command_name: command example to execute --file {{mails}}
```
