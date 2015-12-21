cd `dirname $0`
tshark -l -i '<interface>' -x -f 'host game.fate-go.jp' -Y "data-text-lines contains \"battle_setup\"" | python read_drops.py
