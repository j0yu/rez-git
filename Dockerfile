FROM rockylinux:9.5

RUN dnf install -y \
    "@Development Tools" \
    asciidoc \
    perl-CPAN \
    xmlto \
    curl-devel \
    expat-devel \
    gettext-devel \
    openssl-devel \
    perl-devel \
    tcl-devel \
    tk-devel \
    zlib-devel \
    && dnf clean all
WORKDIR /usr/local/src
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
