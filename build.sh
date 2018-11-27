docker container rm -f gupy-container
docker image build -t gupy .
docker container run --name gupy-container gupy
docker container cp gupy-container:/src/gupy/build/firmware.hex build/