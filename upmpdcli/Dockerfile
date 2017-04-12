FROM debian

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates git build-essential debhelper dh-systemd autoconf automake libtool libupnp6-dev libcurl4-gnutls-dev libmpdclient-dev libexpat1-dev init-system-helpers pkg-config dh-python python libmicrohttpd-dev libjsoncpp-dev

RUN mkdir -p /usr/src && cd /usr/src && \
    git clone https://github.com/medoc92/libupnpp.git && \
    cd libupnpp && \
    ./autogen.sh && \
    dpkg-buildpackage -b -us -uc && \
    dpkg -i ../libupnpp*.deb

RUN mkdir -p /usr/src && cd /usr/src && \
    git clone https://github.com/medoc92/upmpdcli.git && \
    cd upmpdcli && \
    ./autogen.sh && \
    dpkg-buildpackage -b -us -uc && \
    dpkg -i ../upmpdcli_*.deb

RUN useradd -m upmpd

USER upmpd

ADD upmpdcli.conf /etc/

ENV UPMPD_CONFIG /etc/upmpdcli.conf
EXPOSE 6610

ENTRYPOINT ["/usr/bin/upmpdcli"]
