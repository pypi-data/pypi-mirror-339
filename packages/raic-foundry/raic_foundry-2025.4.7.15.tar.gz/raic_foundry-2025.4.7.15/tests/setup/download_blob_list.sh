storage_account=$1
container_name=$2
blob_source_list=$3
blob_destination_folder=$4
blob_destination_folder=$(echo $blob_destination_folder | tr -d '\r')
blob_destination_folder=$(echo $blob_destination_folder | tr -d '\n')

if [ ! -d "$blob_destination_folder" ]; then
    echo "Downloading list of blobs into ${blob_destination_folder}..."

    for line in $(cat ${blob_source_list});
    do
      IFS=$','; split=($line); unset IFS;
      blob_name=$(echo ${split[0]} | tr -d '\r' | tr -d '\n')
      ./setup/download_blob.sh ${storage_account} ${container_name} $blob_name ${blob_destination_folder}/$(basename $blob_name)
    done

else
  echo "${blob_destination_folder} exists locally"
fi
