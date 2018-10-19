#!/bin/bash

BKP_DIR="./backup"
APP_DIR="./wp"

if [ -d "$BKP_DIR" ]; then
    mkdir "$BKP_DIR"
fi

rsync -avz $APP_DIR $BKP_DIR
