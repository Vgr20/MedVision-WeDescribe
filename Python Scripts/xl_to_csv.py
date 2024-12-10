import pandas as pd
import argparse
import os
import csv


def main(input_dir):
    xl_path = input_dir
    csv_path = os.path.splitext(input_dir)[0]+".csv"

    read_file = pd.read_excel(input_dir)
    read_file.to_csv(csv_path,index = None, header=True)

    df = pd.read_csv(csv_path)
    df = df.drop([0,1,8,16])
    df = df.reset_index(drop=True)
    df.to_csv(csv_path,index = None, header=True)
    print(df.head())

    new_headers = ['Para.','Result','Unit','Ref.Ranges']

    with open (csv_path , 'r', newline='') as infile:
        reader = csv.reader(infile)
        data = list(reader)

    data[0] = new_headers


    with open (csv_path , 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)


    df = pd.read_csv(csv_path)
    print(df.head())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--xl_path',metavar='input_directory', type=str, required=True )
    args=parser.parse_args()


main(args.xl_path)
