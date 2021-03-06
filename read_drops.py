#! /usr/bin/python

import json
import fileinput
import sys
from jsonpath_rw import jsonpath, parse

log = open('lastSession', 'w')

class DropManager:
    """Manages item information.

    Expects each item to use its id as the key, and provide its name as the
    property 'name'.
    
    The 'jpName' property is not currrently used, as Windows command prompt
    doesn't play nice with UTF-8.""" 

    def __init__(self):
        self.index = json.load(open('dropIds.json', 'r'))

    def item(self, drop):
        """Convert item data into human readable format.

        Takes a JSON object describing an item that dropped, and returns a
        string describing it."""
        id = str(drop.get("objectId"))
        result = ''
        if id == "1":
            result += 'QP'
            #return "{0} QP".format(drop.get("num"))
        elif id in self.index and 'name' in self.index.get(id):
            result += self.index.get(id).get('name')
        else:
            result += 'Unknown item (ID: {0})'.format(id)

        if drop.get('num') > 1:
            result += ' x{0}'.format(drop.get('num'))

        return result


items = DropManager()

class Parser:
    """Parses tmux output and extracts item drop information.
    
    Because tmux truncates plain-text output, we instead have it do a hex
    dump, extract the hex-part, convert that back into plain-text and then
    parse that as json."""
    def __init__(self):
        self.body = None
        # JSONpath for extracting drop information from response body
        self.path = parse('cache.replaced.battle[*].battleInfo.enemyDeck[*]'
                          '.svts[*].dropInfos[*]')

    def start(self):
        """Mark the start of a parse input."""
        self.body = ''

    def line(self, str):
        """Add some tmux output to the data to be parsed.

        Has no effect if there is no active parse; i.e. it must be called after
        start() and before end()."""
        if self.body is None:
            return
        # strip non-hex data (could also just extract the ascii data)
        res = str[4:-17].strip()
        # decode hex
        self.body += res.replace(' ', '').decode('hex')

    def end(self):
        """Mark input as complete, parse it and output drop information."""
        if self.body is None:
            return
        # Get response body
        body = self.body[self.body.find("{"):]
        # Get drop ids from response body
        drops = []
        res = json.loads(body)
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

    if 'Reassembled' in line:
        parser.start()
    elif not line.strip():
        parser.end()
    else:
        parser.line(line)
