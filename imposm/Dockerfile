FROM golang:1.17

ARG IMPOSM_REPOSITORY="https://github.com/omniscale/imposm3.git"
ARG IMPOSM_VERSION="v0.11.1"

RUN apt-get update && apt-get install  -y \
        libgeos-dev \
        libleveldb-dev \
        libprotobuf-dev \
        protobuf-compiler \
        \
    && go version \
    && cd $GOPATH \
    && go get github.com/tools/godep \
    && git clone $IMPOSM_REPOSITORY -b $IMPOSM_VERSION $GOPATH/src/github.com/omniscale/imposm3 \
    && cd $GOPATH/src/github.com/omniscale/imposm3 \
    && go install ./cmd/imposm/

WORKDIR /go/bin
