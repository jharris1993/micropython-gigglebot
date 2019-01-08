FROM ubuntu:18.04

RUN apt-get update -qq && \
    apt-get install git python python-pip software-properties-common -y
RUN add-apt-repository -y ppa:team-gcc-arm-embedded/ppa && \
    apt-get update && \
    apt-get install gcc-arm-embedded cmake ninja-build srecord libssl-dev -y
RUN pip install yotta git+https://github.com/liftoff/pyminifier

ENV GUPY_HASH=9f79a8e5cabb6d6f94622f830c7495947a938b86

WORKDIR /src/
RUN git clone -b master https://github.com/bbcmicrobit/micropython gupy && \
    cd gupy && git reset --hard ${GUPY_HASH} && cd -
RUN UPY_HASH=$(sed -n '3p' gupy/inc/genhdr/mpversion.h | cut -d\" -f2) && \
    git clone -b master https://github.com/micropython/micropython upy && \
    cd upy && git reset --hard ${UPY_HASH} && cd -

# initialize upy repo
WORKDIR /src/gupy
RUN yt target bbc-microbit-classic-gcc-nosd && \
    yt up

# enable memoryview before running makeqstrhdr.sh
RUN sed -i -e 's/MICROPY_PY_BUILTINS_MEMORYVIEW (0)/MICROPY_PY_BUILTINS_MEMORYVIEW (1)/g' /src/gupy/inc/microbit/mpconfigport.h

# disable speech module to reduce firmware size
# RUN sed -i -e '/MP_ROM_PTR(&love_module)/d' /src/gupy/inc/microbit/mpconfigport.h && \
#     sed -i -e '/MP_ROM_PTR(&antigravity_module)/d' /src/gupy/inc/microbit/mpconfigport.h

# generate qstrhdr
RUN python tools/makeversionhdr.py microbitversion.h && \
    mv microbitversion.h inc/genhdr && \
    ./tools/makeqstrhdr.sh

# remove the compass module from microbit package
RUN rm /src/gupy/source/microbit/microbitcompass.cpp && \
    sed -i -e '/compass_up_to_date/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/compass_updating/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/_microbit_compass_obj_t/d' /src/gupy/inc/microbit/modmicrobit.h && \
    
    sed -i -e '/microbit_compass_init/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_is_calibrated_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_heading_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_calibrate_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_is_calibrating_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_clear_calibration_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_get_x_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_get_y_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_get_z_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_get_field_strength_obj/d' /src/gupy/inc/microbit/modmicrobit.h && \
    sed -i -e '/microbit_compass_obj/d' /src/gupy/source/microbit/modmicrobit.cpp
COPY source/* /src/gupy/source/microbit/
COPY inc/* /src/gupy/inc/microbit/

# enable frozen and bytecoded modules
RUN sed -i '1s/^/#define MICROPY_QSTR_EXTRA_POOL (mp_qstr_frozen_const_pool)\n/' /src/gupy/inc/microbit/mpconfigport.h && \
    sed -i '2s/^/#define MICROPY_MODULE_FROZEN_MPY (1)\n/' /src/gupy/inc/microbit/mpconfigport.h && \
    sed -i '3s/^/#define MICROPY_PERSISTENT_CODE_LOAD (1)\n/' /src/gupy/inc/microbit/mpconfigport.h

WORKDIR /src/gupy
# remove the last 6 lines that contain mp_lexer_new_from_file function
# better alternative with regex here: https://regexr.com/43nbb
RUN head -n -6 source/microbit/filesystem.c > tmp && mv tmp source/microbit/filesystem.c

# and add 2 other functions to the end of it (used to enable the use of mpy files)
RUN echo '\n\
void mp_reader_new_file(mp_reader_t *reader, const char *filename) {\n\
    file_descriptor_obj *fd = microbit_file_open(filename, strlen(filename), false, false);\n\
    if (fd == NULL) {\n\
        mp_raise_OSError(MP_ENOENT);\n\
    }\n\
    reader->data = fd;\n\
    reader->readbyte = file_read_byte;\n\
    reader->close = (void(*)(void*))microbit_file_close;\n\
}\n\
\n\
mp_lexer_t *mp_lexer_new_from_file(const char *filename) {\n\
    mp_reader_t reader;\n\
    mp_reader_new_file(&reader, filename);\n\
    return mp_lexer_new(qstr_from_str(filename), reader);\n\
}\n' >> source/microbit/filesystem.c

# build tool to produce bytecodes of python scripts
WORKDIR /src/upy/mpy-cross
RUN make && cp ./mpy-cross /usr/bin

# create the bytecode for our modules
WORKDIR /src/tmp
COPY *.py ./
RUN for module in $(ls *.py); do pyminifier $module > tmp.py || exit 1; rm $module && mv tmp.py $module; done
RUN for module in $(ls *.py); do mpy-cross $module || exit 1; done

# generate the c code of our module and place it in the right dir to be compiled
RUN python /src/upy/tools/mpy-tool.py -f -q /src/gupy/inc/genhdr/qstrdefs.preprocessed.h *.mpy > /src/gupy/source/py/frozen_module.c

# compile the firmware
WORKDIR /src/gupy
RUN make all

# print out the number of bytes used by the firmware
RUN stat --printf='%s' build/bbc-microbit-classic-gcc-nosd/source/microbit-micropython.bin > /src/tmp/usedspace.txt