#!/bin/bash

set +eu

./build.sh
docker run -p 5555:5555 hector 

