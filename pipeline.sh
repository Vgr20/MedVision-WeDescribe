#!/bin/bash
#
#

echo "--------------------------------------Entering Table_detection---------------------------------------"

cd /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/table_detection


echo "---------------------------------------Starting Table_detection---------------------------------------"

IMAGE_DIR="../images"

echo "------------------------------------------Images available-------------------------------------------"

for image_file in "$IMAGE_DIR"/*.jpg;
do
  echo "$image_file"
done

for image_file in "$IMAGE_DIR"/*.jpg;
do
  python3 inference.py --inputDIR "$image_file" > /dev/null 2>&1
  echo "------------------------------------Table Detected Successfully----------------------------------"
done


cd ..

cd /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/trocr/PaddleOCR/ppstructure

bash detect.sh

cd ../../..

echo "---------------------------------Changing .xlsx files .csv---------------------------------"

XL_DIR='./extracted_tables'

for xl_file in "$XL_DIR"/*.xlsx;
do 
  echo "$xl_file"
done


for xl_file in "$XL_DIR"/*.xlsx;
do 
  python3 xl_to_csv.py --xl_path "$xl_file" > /dev/null 2>&1
  echo "--------------------------------------Converting to .csv completed --------------------"
done

cd /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/sent_ana

CSV_DIR='../extracted_tables'

for csv_file in "$CSV_DIR"/*.csv;
do
  echo "$csv_file"
done


for csv_file in "$CSV_DIR"/*.csv;
do
  python3 text_extractor.py --inputDIR "$csv_file" > /dev/null 2>&1
  echo "------------------------------------Probability Generated Successfully----------------------------------"
done

echo "--------------------------------------Entering Text Generation---------------------------------------"

cd /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/text_generation

TABLE_DIR="../extracted_tables"

echo "------------------------------------------Tables available-------------------------------------------"

for table_file in "$TABLE_DIR"/*.csv;
do
  echo "$table_file"
done

echo "---------------------------------------Starting Text Generation---------------------------------------"

for table_file in "$TABLE_DIR"/*.csv;
do
  echo "$table_file"
  python3 inference.py --path "$table_file" > /dev/null 2>&1
  echo "------------------------------------Text Generated Successfully----------------------------------"
done

echo "------------------------------------End of Text Generation----------------------------------"

echo "---------------------------------------Starting of Overall Expression Image Generation---------------------------------------"

cd /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/image_generation

python3 overall_expression.py \
        --prob_path /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/senta_ana_output/senta_ana_pred.json \
        --save_dir /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/expression_images 

echo "---------------------------------------End of Overall Expression Image Generation---------------------------------------"

CSV_DIR="../extracted_tables"

echo "------------------------------------Available CSV files----------------------------------"

for csv_file in "$CSV_DIR"/*.csv;
do
  echo "$csv_file"
done

echo "------------------------------------Starting of Gauge Image Generation----------------------------------"

for csv_file in "$CSV_DIR"/*.csv;
do
  echo "$csv_file"
  python3 gauge_generation.py \
          --csv_file "$csv_file" \
          --save_dir /content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/gauge_images 
  echo "------------------------------------Gauge Image Generated Successfully----------------------------------"
done

echo "------------------------------------End of Image Generation----------------------------------"





