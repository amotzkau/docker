FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates git build-essential libasound2-dev libvorbisidec-dev libvorbis-dev libflac-dev libopus-dev libsoxr-dev libboost-dev alsa-utils libavahi-client-dev avahi-daemon curl

RUN git clone https://github.com/badaix/snapcast.git && \
    git -C snapcast/externals submodule update --init --recursive && \
    make -C snapcast/server && \
    make -C snapcast/server install && \
    rm -rf snapcast

ADD snapserver.conf /etc

RUN useradd -m snapcast

USER snapcast

EXPOSE 1704
EXPOSE 1705
EXPOSE 1780

ENTRYPOINT ["/usr/bin/snapserver"]
