#!/bin/bash

# create folder structure
mkdir -p detected_tables
mkdir -p extracted_tables
mkdir -p expression_images
mkdir -p gauge_images
mkdir -p outputs
mkdir -p senta_ana_output

# download data stream
gdown "https://drive.google.com/uc?id=1nEm_lrNZ75rNT58FRyttacMNtQHkvcNt" -O data_stream.zip
unzip data_stream.zip
rm data_stream.zip

# download input images
gdown "https://drive.google.com/uc?id=1bj7jXJ34FfOBuY-pNISsF8J0GOCgcnE4" -O images.zip
unzip images.zip
rm images.zip

echo "Initialization complete"

