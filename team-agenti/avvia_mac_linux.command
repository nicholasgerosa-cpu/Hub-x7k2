#!/bin/sh
# Mac/Linux: doppio clic (Mac) oppure ./avvia_mac_linux.command dal terminale
cd "$(dirname "$0")" || exit 1
exec python3 team_agenti.py "$@"
