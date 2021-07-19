FROM centos:7

RUN yum install -y \
    "@Development Tools" \
    asciidoc \
    dblatex \
    docbook2X \
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
    && ln -vs /usr/bin/db2x_docbook2texi /usr/bin/docbook2x-texi \
    && yum clean all
WORKDIR /usr/local/src
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]