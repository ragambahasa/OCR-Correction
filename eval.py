import os
import re
import jellyfish
import pandas as pd
import argparse

from jiwer import wer, cer, mer
from datetime import datetime

def compile_dataset(gt_dir, engine_dir, **kwargs):
    
    gt_listdir = os.listdir(gt_dir)
    gt_dataset = [ os.path.join(gt_dir, d) for d in gt_listdir ]
    
    engine_listdir = os.listdir(engine_dir)
    engine_dataset = [ os.path.join(engine_dir, d) for d in engine_listdir ]

    gt_texts = []
    for gt in gt_dataset:
        with open(gt, "r", encoding="utf-8") as f:
            filename = os.path.basename(gt)
            text = f.read()
            gt_texts.append({"entry_name": filename.split(".")[0], "filename": gt, "text_gt": text})


    engine_texts = []
    for engine in engine_dataset:
        with open(engine, "r", encoding="utf-8") as f:
            filename = os.path.basename(engine)
            text = f.read()
            engine_texts.append({"entry_name": filename.split(".")[0], "filename": engine, "text_engine": text})
    
    gtdf = pd.DataFrame(gt_texts)
    gtdf = gtdf.sort_values(by=['entry_name'])
    
    enginedf = pd.DataFrame(engine_texts)
    enginedf = enginedf.sort_values(by=['entry_name'])

    df = pd.merge(gtdf, enginedf, on=['entry_name'], suffixes=['_gt', '_engine'])
    df = df.sort_index(axis=1)

    if kwargs.get('export'):

        if not os.path.exists(kwargs['export']):
            os.makedirs(kwargs['export'])

        filename = f"compiled_data_{datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')}.csv"
        filename = os.path.join(kwargs['export'], filename)
        df.to_csv(filename, sep=";")
    return df

def evaluation_metrics(df, **kwargs):
    df['max_len'] = df.apply(lambda x: max(tuple((len(x['text_engine']), len(x['text_gt'])))), axis=1)
    df['levd'] = df.apply(lambda x: jellyfish.levenshtein_distance(x['text_engine'], x['text_gt']), axis=1)
    # df['levd_wer'] = df.apply(lambda x: 1-x['levd']/len(x['text_gt']), axis=1)
    df['levd_score'] = df.apply(lambda x: 1-x['levd']/x['max_len'], axis=1)

    df['wer'] = df.apply(lambda x: 1-wer(x['text_gt'], x['text_engine']), axis=1)
    df['cer'] = df.apply(lambda x: 1-cer(x['text_gt'], x['text_engine']), axis=1)
    df['mer'] = df.apply(lambda x: 1-mer(x['text_gt'], x['text_engine']), axis=1)

    if kwargs.get('export'):

        if not os.path.exists(kwargs['export']):
            os.makedirs(kwargs['export'])

        filename = f"eval_data_{datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')}.csv"
        filename = os.path.join(kwargs['export'], filename)
        df.to_csv(filename, sep=";")
    
    wer_avg = df['wer'].mean()
    cer_avg = df['cer'].mean()
    mer_avg = df['mer'].mean()
    levd_score_avg = df['levd_score'].mean()

    wer_min = df['wer'].min()
    cer_min = df['cer'].min()
    mer_min = df['mer'].min()
    levd_score_min = df['levd_score'].min()

    wer_max = df['wer'].max()
    cer_max = df['cer'].max()
    mer_max = df['mer'].max()
    levd_score_max = df['levd_score'].max()

    wer_mix = df.loc[df['wer'].idxmin()]
    cer_mix = df.loc[df['cer'].idxmin()]
    mer_mix = df.loc[df['mer'].idxmin()]
    levd_score_mix = df.loc[df['levd_score'].idxmin()]

    print(f"WER Average: {wer_avg:.4f}, Min: {wer_min:.4f}, Max: {wer_max:.4f}, Mix: {wer_mix['wer']:.4f}")
    print(f"CER Average: {cer_avg:.4f}, Min: {cer_min:.4f}, Max: {cer_max:.4f}, Mix: {cer_mix['cer']:.4f}")
    print(f"MER Average: {mer_avg:.4f}, Min: {mer_min:.4f}, Max: {mer_max:.4f}, Mix: {mer_mix['mer']:.4f}")
    print(f"Levenshtein Score Average: {levd_score_avg:.4f}, Min: {levd_score_min:.4f}, Max: {levd_score_max:.4f}, Mix: {levd_score_mix['levd_score']:.4f}")

    return df

def main():
    parser = argparse.ArgumentParser(description="Run Evaluation")
    parser.add_argument("-ann", type=str, required=True, help="Folder containing human annotation txt files")
    parser.add_argument("-ots", type=str, required=True, help="Folder containing plain ocr txt files")
    parser.add_argument("-post", type=str, required=True, help="Folder containing post ocr correction txt files")
    
    args = parser.parse_args()

    TEST_OTS_DIR = f"{args.ots}"
    TEST_ANN_DIR = f"{args.ann}"
    TEST_CORRECTION_DIR = f"{args.post}"

    print("POST OCR")
    compiled = compile_dataset(gt_dir=TEST_ANN_DIR, engine_dir=TEST_CORRECTION_DIR)
    evaluate = evaluation_metrics(df=compiled, export="eval-result")
    print("\nOTS")
    compiled = compile_dataset(gt_dir=TEST_ANN_DIR, engine_dir=TEST_OTS_DIR)
    evaluate = evaluation_metrics(df=compiled, export="eval-result")
    
if __name__ == "__main__":
    main()