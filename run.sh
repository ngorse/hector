#!/bin/bash

set +eu

docker build -t hector .
docker run -p 5555:5555 hector 

