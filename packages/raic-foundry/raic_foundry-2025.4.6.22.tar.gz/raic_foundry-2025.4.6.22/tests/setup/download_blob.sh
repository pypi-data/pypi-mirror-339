storage_account=$1
container_name=$2
blob_source=$3
blob_destination=$4

if [ ! -f "$blob_destination" ]; then
    echo "Downloading ${blob_destination} from ${blob_source}..."

    mkdir -p $(dirname ${blob_destination})

    az storage blob download \
        --account-name ${storage_account} \
        --container-name ${container_name} \
        --name ${blob_source} \
        --file ${blob_destination} \
        --max-connections 6 \
        --auth-mode key
else
  echo "${blob_destination} exists locally"
fi
