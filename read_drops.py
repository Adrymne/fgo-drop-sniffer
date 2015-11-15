#! /usr/bin/python

import json
import fileinput
import sys

class DropManager:
    def __init__(self, file):
        self.index = json.load(open(file, 'r'))

    def item(self, drop):
        id = str(drop["objectId"])
        if id == "1":
            return "{0} QP".format(drop["num"])
        elif id in self.index:
            item = self.index[id]
            result = item["name"] 
            #if "jpName" in item:
            #    result += u" ({0})".format(item["jpName"])
            return result
        else: 
            return "Unknown item (ID: {0})".format(id)

items = DropManager('dropIds.json')

class Parser:
    def __init__(self):
        self.body = None

    def start(self):
        self.body = ''

    def line(self, str):
        if self.body is None:
            return
        # strip non-hex data
        res = str[4:-17].strip()
        # decode hex
        self.body += res.replace(' ', '').decode('hex')

    def end(self):
        if self.body is None:
            return
        # Get drop ids from response body
        drops = []
        res = json.loads(self.body)
        for battle in res["cache"]["replaced"]["battle"]:
            for deck in battle["battleInfo"]["enemyDeck"]:
                for svt in deck["svts"]:
                    drops.extend([items.item(drop) for drop in svt["dropInfos"]])
        # Print out drops
        print "-" * 20
        if len(drops) == 0:
            print "[No drops]"

        for drop in drops:
            print drop
        self.body = None

parser = Parser()

while True:
    line = sys.stdin.readline()

    if 'Uncompressed entity body' in line:
        parser.start()
    elif not line.strip():
        parser.end()
    else:
        parser.line(line)
