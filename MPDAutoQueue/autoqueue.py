#! /usr/bin/python3

import musicpd
import argparse, time, socket, random

parser = argparse.ArgumentParser(description="Automatically add songs to the MPD queue", add_help=False)
parser.add_argument("--help", help="show this help message and exit", action="help")
parser.add_argument("-h", "--host", help="MPD host name (default: localhost)", default="localhost")
parser.add_argument("-p", "--port", help="MPD port (default: 6600)", type=int, default=6600)
parser.add_argument("-q", "--quiet", help="Silent mode", action="store_true", default=False)
parser.add_argument("-l", "--playlist", metavar="PLAYLIST[:WEIGHT]", help="Takes songs from this playlist (default: Auto)", action="append", default=[])
parser.add_argument("-b", "--before", help="How many played songs leave in the playlist (default: 10)", type=int, default=10)
parser.add_argument("-a", "--ahead", help="How many songs plan ahead (default: 10)", type=int, default=10)

args = parser.parse_args()
client = musicpd.MPDClient()

currentlists = {}    # { 'playlist', 'last-modified', 'weight' }
currentsongs = []    # [ (id, name) ]
playedsongs =  []    # [ id ]

if not len(args.playlist):
    args.playlist.append('Auto')

def msg(*msg):
    if not args.quiet:
        print(*msg)

def parsePlaylist(name):
    values = name.rsplit(":", 1)
    if len(values) == 2:
        try:
            return (values[0], int(values[1]))
        except ValueError:
            msg("Could not parse '%s'" % (name,))
            return (values[0],1)
    else:
        return (name, 1,)

def waitForAutoMode():
    while True:
        status = client.status()
        if int(status['random']):
            msg("Random mode is activated, waiting for deactivation...")
        elif int(status['repeat']):
            msg("Repeat mode is activated, waiting for deactivation...")
        elif int(status['single']):
            msg("Single mode is activated, waiting for deactivation...")
        else:
            break
        client.idle('options')


def updateSongList():
    global currentsongs
    global currentlists
    global playedsongs

    lists = { entry['playlist']: entry for entry in client.listplaylists() }

    dirty = False
    newlists = {}
    for (listname, weight) in args.playlist:
        if listname in lists:
            dirty = (not listname in currentlists or currentlists[listname]['last-modified'] != lists[listname]['last-modified'])
            newlists[listname] = lists[listname]
            newlists[listname]['weight'] = weight
        else:
            msg("Unknown playlist '%s'." % listname)

    if dirty:
        newsongs = []
        for playlist in newlists.values():
           newsongs.extend(playlist['weight'] * client.listplaylist(playlist['playlist']))

        currentlists = newlists
        currentsongs = list(zip(range(len(newsongs)), newsongs))
        playedsongs = []


def chooseSong():
    global currentsongs
    global playedsongs

    while 2*len(playedsongs) > len(currentsongs):
        playedsongs.pop(0)

    pos = random.randrange(len(currentsongs) - len(playedsongs))
    i = 0
    while True:
        if not currentsongs[i][0] in playedsongs:
            pos -= 1
            if pos < 0:
                break
        i += 1

    playedsongs.append(currentsongs[i][0])
    return currentsongs[i][1]


def updatePlaylist():
    status = client.status()
    pos = int(status['song'])
    length = int(status['playlistlength'])

    client.command_list_ok_begin()

    if pos > args.before:
        client.delete((0,pos - args.before))

    for i in range(length - pos - 1, args.ahead):
        client.add(chooseSong())

    client.command_list_end()

args.playlist = [ parsePlaylist(entry) for entry in args.playlist ]

try:
    while True:
        try:
            msg("Connecting to %s:%d..." % (args.host, args.port))
            client.connect(args.host, args.port)
            msg("Connected to MPD %s." % (client.mpd_version,))

            while True:
                waitForAutoMode()
                updateSongList()

                if len(currentsongs):
                    updatePlaylist()
                client.idle('stored_playlist', 'playlist', 'player')

        except socket.error as e:
            msg('Error:', e)
            time.sleep(1)
        except musicpd.ConnectionError as e:
            msg('Error:', e)
            time.sleep(1)
except KeyboardInterrupt:
    client.close()

client.disconnect()
