#!/usr/bin/env bash

ot_project=open-targets-genetics

if [ $# -ne 1 ]; then
    echo "Usage: $0 <tag-name>"
    exit 1
fi

gcloud compute instances create be-debian-worker-$1  \
       --image-project debian-cloud \
       --image-family debian-9 \
       --machine-type n1-highmem-4 \
       --zone europe-west1-d \
       --metadata-from-file startup-script=debian_worker.sh \
       --boot-disk-size "25" \
       --boot-disk-type "pd-ssd" \
       --project $ot_project \
       --preemptible \
       --scopes default,storage-rw

# --metadata es_server=http://10.132.0.3:9200,es_prefix=mkes5.2

# --boot-disk-device-name "ot-es550" \
