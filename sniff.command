cd `dirname $0`
tshark -l -i '<interface>' -x -f 'host fgo-game-jpe.cloudapp.net' -Y "data-text-lines contains \"battle_setup\"" | python read_drops.py
