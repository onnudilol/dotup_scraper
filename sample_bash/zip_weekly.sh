#!/bin/bash

now=$(date +"week_%U_%d-%m-%Y")
mkdir -p weekly/
zip -r weekly/${now}.zip daily/*
rm -rf daily/*
