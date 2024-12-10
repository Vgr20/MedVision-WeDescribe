import torch
import pandas as pd
import argparse
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline


def main(input_dir):
    file_path = input_dir
    df = pd.read_csv(file_path)

    param = df['Para.']
    results = df['Result']
    ref = df['Ref.Ranges']

    def check_range(results, ref):
        if pd.isna(ref):
            return 'Neutral'
        else:
            min_val, max_val = map(float, ref.split('-'))
        return min_val <= float(results) <= max_val

    df['out'] = df.apply(lambda row: check_range(row['Result'], row['Ref.Ranges']), axis=1)

    out_test = ""

    for x in range(df.shape[0]):
        if df['out'][x]:
            out_test += "your " + str(param[x]) + " levels are good. "
        elif df['out'][x] == 'Neutral':
            out_test += "your " + str(param[x]) + " levels are neither good or bad. "
        else:
            out_test += "your " + str(param[x]) + " levels are bad. "

    model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
    tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")

    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    results = nlp(out_test)
    print("Overall Result: ", results[0]["label"])
    print("Overall Probability of positiveness: ", results[0]["score"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process some files in the directory')
    parser.add_argument('--inputDIR', metavar='input_directory', type=str, required=True)
    args = parser.parse_args()

main(args.inputDIR)
