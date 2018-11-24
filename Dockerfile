FROM ubuntu:18.04

RUN apt-get update -qq && \
    apt-get install git python python-pip software-properties-common -y
RUN add-apt-repository -y ppa:team-gcc-arm-embedded/ppa && \
    apt-get update && \
    apt-get install gcc-arm-embedded cmake ninja-build srecord libssl-dev -y
RUN pip install yotta

ENV GUPY_HASH=b60f1382667aa86909a433aab9ba2739f4f71de3

WORKDIR /src/
RUN git clone -b master https://github.com/bbcmicrobit/micropython gupy && \
    cd gupy && git reset --hard ${GUPY_HASH} && cd -
RUN UPY_HASH=$(sed -n '3p' gupy/inc/genhdr/mpversion.h | cut -d\" -f2) && \
    git clone -b master https://github.com/micropython/micropython upy && \
    cd upy && git reset --hard ${UPY_HASH} && cd -

# initialize uy repo
WORKDIR /src/gupy
RUN yt target bbc-microbit-classic-gcc-nosd && \
    yt up

# generate qstrhdr
RUN python tools/makeversionhdr.py microbitversion.h && \
    mv microbitversion.h inc/genhdr && \
    ./tools/makeqstrhdr.sh

# build tool to produce bytecodes of python scripts
WORKDIR /src/upy/mpy-cross
RUN make && cp ./mpy-cross /usr/bin

# create the bytecode for our module
WORKDIR /src/tmp
COPY src/perf.py .
RUN mpy-cross perf.py

# generate the c code of our module
RUN python /src/upy/tools/mpy-tool.py -f -q /src/gupy/inc/genhdr/qstrdefs.preprocessed.h perf.mpy > frozen_module.c

