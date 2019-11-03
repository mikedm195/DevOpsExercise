#!/usr/bin/env bash

sleep 5
mongo_ip=`ping -c1 mongodb | head -1 | cut -d ' ' -f 3 | tr -d '():'`

mongoimport --host $mongo_ip --db sample_library --collection books --type json --file /mongo_dataset/books.json --upsert
