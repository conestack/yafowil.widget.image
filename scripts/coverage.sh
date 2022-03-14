#!/bin/sh

set -e

./bin/coverage run \
    --source src/yafowil/widget/image \
    --omit src/yafowil/widget/image/example.py \
    -m yafowil.widget.image.tests
./bin/coverage report
./bin/coverage html
