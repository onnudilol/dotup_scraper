#!/bin/bash

now=$(date +"%b_%Y")
mkdir -p monthly/
zip monthly/${now}.zip weekly/*
rm -rf weekly/*
