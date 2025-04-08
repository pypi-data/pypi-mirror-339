
DESTINATION_ROOT_FOLDER='.ignore'

# Login to Azure
az cloud set --name AzureCloud
#az login


echo
echo
echo '***************************************************************************'
echo 'Downloading models...'
echo '***************************************************************************'

MODEL_STORAGE_ACCOUNT='pretrainedmodels001'
MODEL_CONTAINER='metadetectors'
VECTORIZER_CONTAINER='pytorch'
VECTORIZER_MODEL_NAME='vit-dino/vits16_orig_pretrained.pth'
DESTINATION_FOLDER="${DESTINATION_ROOT_FOLDER}/models"

./setup/download_blob.sh ${MODEL_STORAGE_ACCOUNT} ${MODEL_CONTAINER} 'yolov5/weights/XVIEW_single_cls_best.pt' ${DESTINATION_FOLDER}/general_geo_objects.pt
./setup/download_blob.sh ${MODEL_STORAGE_ACCOUNT} ${MODEL_CONTAINER} 'yolov5/weights/yolov5l6.pt' ${DESTINATION_FOLDER}/generic_objects_detector.pt
./setup/download_blob.sh ${MODEL_STORAGE_ACCOUNT} ${MODEL_CONTAINER} 'yolov5/weights/traffic_signs_v1.pt' ${DESTINATION_FOLDER}/traffic_signs_v1.pt

./setup/download_blob.sh ${MODEL_STORAGE_ACCOUNT} ${VECTORIZER_CONTAINER} ${VECTORIZER_MODEL_NAME} ${DESTINATION_FOLDER}/vits16_orig_pretrained.pth
mv ${DESTINATION_FOLDER}/vits16_orig_pretrained.pth ${DESTINATION_FOLDER}/vectorizer16.pth

MODEL_CONTAINER='registered-models'
./setup/download_blob.sh ${MODEL_STORAGE_ACCOUNT} ${MODEL_CONTAINER} '10_sign_detection_yolov5.pt' ${DESTINATION_FOLDER}/10_sign_detection_yolov5.pt
./setup/download_blob.sh ${MODEL_STORAGE_ACCOUNT} ${MODEL_CONTAINER} '10_sign_detection_yolov8.pt' ${DESTINATION_FOLDER}/10_sign_detection_yolov8.pt


echo
echo
echo '***************************************************************************'
echo 'Downloading test imagery...'
echo '***************************************************************************'

IMAGERY_STORAGE_ACCOUNT='customerdatastoragescus'
IMAGERY_CONTAINER='trimble'
DESTINATION_FOLDER="${DESTINATION_ROOT_FOLDER}/datasources"

# Trimble 1
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001193.jpg' ${DESTINATION_FOLDER}/trimble_1/pano_000002_001193.jpg

# Trimble 3
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001193.jpg' ${DESTINATION_FOLDER}/trimble_3/pano_000002_001193.jpg
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001194.jpg' ${DESTINATION_FOLDER}/trimble_3/pano_000002_001194.jpg
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001195.jpg' ${DESTINATION_FOLDER}/trimble_3/pano_000002_001195.jpg

# Trimble 3 Archived
mkdir ${DESTINATION_FOLDER}/trimble_3_tar
if [ ! -f "${DESTINATION_FOLDER}/trimble_3_tar/trimble_3.tar" ]; then
    (cd ${DESTINATION_FOLDER} && tar cvf trimble_3_tar/trimble_3.tar trimble_3/*.jpg)
fi

mkdir ${DESTINATION_FOLDER}/trimble_3_zip
if [ ! -f "${DESTINATION_FOLDER}/trimble_3_zip/trimble_3.zip" ]; then
    (cd ${DESTINATION_FOLDER} && zip trimble_3_zip/trimble_3.zip trimble_3/*.jpg)
fi

# Trimble 3 Nested Folders
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001193.jpg' ${DESTINATION_FOLDER}/trimble_3_nested/nested-1/nested_a/pano_000002_001193.jpg
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001194.jpg' ${DESTINATION_FOLDER}/trimble_3_nested/nested-1/nested_b/pano_000002_001194.jpg
./setup/download_blob.sh ${IMAGERY_STORAGE_ACCOUNT} ${IMAGERY_CONTAINER} 'Imagery/20240306/pano_000002_001195.jpg' ${DESTINATION_FOLDER}/trimble_3_nested/nested-1/nested_c/pano_000002_001195.jpg