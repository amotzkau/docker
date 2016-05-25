# Docker Repository

This is just my repository for some personal docker images.

## MPD

Installs MPD (the music player daemon) from the current official debian image.
The configuration has three outputs:
 * ALSA
 * HTTP Stream (ogg vorbis), Port 8000
 * PCM Stream in /fifo/pcmstream

The following volumes are exported:
 * /music: Contains the music files
 * /playlists: Contains the playlists files
 * /db: The music database (and state information)
 * /fifo: Contains the PCM stream

Also the command port 6600 is exposed.

## MPDAutoQueue

Simple Python script that automatically randomly enqueues songs from the playlist
'Auto' into MPD.

## Snapcast

Fetches and builds the latest snapcast server (https://github.com/badaix/snapcast).
Call with `-s 'pipe:///fifo/pcmstream?name=MPD'` and import the /fifo volume from MPD
to stream its music.

## upmpdcli

Fetches and builds the latest upmpdcli (https://github.com/medoc92/upmpdcli).
