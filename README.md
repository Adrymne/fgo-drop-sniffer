**Prerequisites**

* [Python 2.7.x](https://www.python.org/downloads/release/python-2710/) (it may work on other versions; I haven't tested it and make no guarantees)
* [Wireshark](https://www.wireshark.org/#download)

**Setup**

`tshark -l -i "Wi-Fi" -x -f "host fgo-game-jpe.cloudapp.net" -Y "data-text-lines contains \"battle_setup\"" | python read_drops.py`

Where `"Wi-Fi"` is replaced by whatever interface your computer is using (you can retrieve interfaces with `tshark -D`).

**New Items**

When DW adds new items, the script won't know about them; instead, you'll get output looking like:

`Unknown item (ID: 9400520)`

That's easy enough to fix. Open up the `dropIds.json` file in your editor of choice and add a new entry at the top. The format is:

`"<id>": { "name": "<item name>" }`