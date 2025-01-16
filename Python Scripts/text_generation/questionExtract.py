import pandas as pd
import os

def combine_words(row):
    return f"What does the Full Blood Count report parameter '{row[0]}' mean in a simple sentence for a patient? And for a patient having a {row[0]} parameter of {row[1]}  considering the reference range {row[3]} , what could be the state of the patient in a simple sentence?"

def question_creation(tabel_df_path):
    df = pd.read_csv(tabel_df_path)
    df['combined'] = df.apply(combine_words, axis=1)
    return df

def prompt_list(path):
    df = question_creation(path)
    prompt_dict = {}
    for i in range(df.shape[0]):
      prompt = f""" use following format to give answers
                              Here's some examples for this,

                              <|User|>: What does the Full Blood Count report parameter 'PLATELET COUNT' mean in a simple sentence for a patient? And for a patient having a PLATELET COUNT parameter of 500  considering the reference range 150-400 , what could be the state of the patient in a simple sentence?

                              <|Assistant|>: The 'Platelet Count' in your blood test measures how many platelets you have, which are tiny cells that help stop bleeding if you get a cut. The 'Platelet Count' value is higher than the normal range, which could be an indication of a condition known as 'Thrombosis'.

                              <|User|>: What does the Full Blood Count report parameter 'PLATELET COUNT' mean in a simple sentence for a patient? And for a patient having a PLATELET COUNT parameter of 200  considering the reference range 150-400 , what could be the state of the patient in a simple sentence?

                              <|Assistant|>: The 'Platelet Count' in your blood test measures how many platelets you have, which are tiny cells that help stop bleeding if you get a cut. The 'Platelet Count' value is within the normal range.

                              <|User|>: What does the Full Blood Count report parameter 'PLATELET COUNT' mean in a simple sentence for a patient? And for a patient having a PLATELET COUNT parameter of 100  considering the reference range 150-400 , what could be the state of the patient in a simple sentence?

                              <|Assistant|>: The 'Platelet Count' in your blood test measures how many platelets you have, which are tiny cells that help stop bleeding if you get a cut. The 'Platelet Count' value is less than the normal range, which could be an indication of a condition known as "thrombocytopenia ", can lead to bleeding problems.

                              <|User|>: {df.iloc[i]['combined']}

                              Answers change according to the blood report attribute and if you don't know the cause of the outside of the attribute value. Then, only give whether the attribute value is lower than or greater than or within the normal region precisely.
                              Give me highly accurate and reliable answer for last question."""

      prompt_dict[df.iloc[i,0]] = prompt  
    return prompt_dict
