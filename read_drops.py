#! /usr/bin/python

import json
import fileinput
import sys
from jsonpath_rw import jsonpath, parse

class DropManager:
    def __init__(self, file):
        self.index = json.load(open(file, 'r'))

    def item(self, drop):
        id = str(drop.get("objectId"))
        if id == "1":
            return "{0} QP".format(drop.get("num"))
        elif id in self.index:
            item = self.index.get(id)
            if item and 'name' in item:
                return item.get('name')

        return "Unknown item (ID: {0})".format(id)

items = DropManager('dropIds.json')

class Parser:
    def __init__(self):
        self.body = None
        self.path = parse('cache.replaced.battle[*].battleInfo.enemyDeck[*]'
                          '.svts[*].dropInfos[*]')

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
        drops = [items.item(match.value) for match in self.path.find(res)]
        # Print out drops
        print "-" * 20
        if len(drops) == 0:
            print "[No drops]"
        else: 
            for drop in drops:
                print drop
        # Mark end of parse
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
