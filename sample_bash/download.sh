#!/bin/bash

now=$(date +"%d-%m-%Y")
mkdir -p daily/${now}
wget -nc --limit-rate=128k --wait=60 --random-wait --max-redirect 0 --directory-prefix=daily/${now} -i url_list.txt
