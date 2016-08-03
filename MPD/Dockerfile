FROM debian:jessie-backports

RUN apt-get update && apt-get install -t jessie-backports -y --no-install-recommends mpd libasound2-plugins

RUN mkdir /music /playlists /db /fifo && \
    chown -R mpd:audio /music /playlists /db /fifo

ADD mpd.conf /etc/

USER mpd

EXPOSE 6600
EXPOSE 8000

VOLUME /music
VOLUME /playlists
VOLUME /db
VOLUME /fifo

ENTRYPOINT ["/usr/bin/mpd","--no-daemon"]
