import os
import pandas as pd
import json
import argparse
import random

from difflib import SequenceMatcher

def longest_common_substring(str1, str2):
    """Returns the length of the longest common substring between str1 and str2."""
    match = SequenceMatcher(None, str1, str2).find_longest_match(0, len(str1), 0, len(str2))
    return match.size

def k_most_similar_words(word, dictionary, k, threshold):
    """Returns the similar words from the dictionary based on the longest common substring distance that meet the threshold."""
    word_lower = word.lower()
    similarities = [(dict_word, longest_common_substring(word_lower, dict_word.lower())) for dict_word in dictionary]
    
    # Filter by threshold
    filtered_similarities = [item for item in similarities if (item[1] / len(word)) >= threshold]
    
    # Find exact matches within dictionary words
    exact_matches = []
    for dict_word in dictionary:
        index = dict_word.lower().find(word_lower)
        if index != -1:
            exact_matches.append((dict_word[index:index+len(word)], len(word)))
    
    # Combine exact matches and filtered similarities
    combined_similarities = exact_matches + filtered_similarities
    combined_similarities.sort(key=lambda x: (-x[1], len(x[0])))

    return combined_similarities[:k]

def apply_case(original, word):
    """Applies the case of the original word to the dictionary word."""
    return ''.join(
        dict_char.upper() if orig_char.isupper() else dict_char.lower() 
        for orig_char, dict_char in zip(original, word)
    )

def load_dictionary(dictionary_path):
    """Loads the dictionary from an Excel file."""
    df = pd.read_excel(dictionary_path)
    return df['input'].astype(str).tolist()

def find_similar_words_in_text(input_text, dictionary, k=3, threshold=0.8):
    """Finds the similar dictionary words for each token in the input text that meet the threshold."""
    result = {}
    tokens = input_text.split()
    
    for token in tokens:
        similar_words = k_most_similar_words(token, dictionary, k, threshold)
        if similar_words:
            result[token] = [apply_case(token, word) for word, _ in similar_words]
    
    return result

def process_files(input_folder, output_folder, dictionary_path, k=3, threshold=0.8):
    dictionary = load_dictionary(dictionary_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, filename.replace('.txt', '.json'))
            
            with open(input_filepath, 'r', encoding='utf-8') as file:
                input_text = file.read().strip()
            
            result = find_similar_words_in_text(input_text, dictionary, k, threshold)
            
            output_data = []
            for key, values in result.items():
                output_data.append({"input": key, "output": ','.join(values)})

            if len(output_data) > 10:
                output_data = random.sample(output_data, 10)

            with open(output_filepath, 'w', encoding='utf-8') as f:
                for item in output_data:
                    json.dump(item, f)
                    f.write("\n")
                print(f"Generated file: {output_filepath}")

def main():
    parser = argparse.ArgumentParser(description="Word List Maker for Few Shot OCR Correction")
    parser.add_argument("-ots_folder", type=str, required=True, help="OCR Plain Output.")
    parser.add_argument("-output", type=str, required=True, help="JSON Examples Output Directory.")
    parser.add_argument("-dict", type=str, required=True, help="Dictionary Path.")
    parser.add_argument("-k", type=int, required=True, help="K value for the maximum similar words.")
    parser.add_argument("-t", type=float, required=True, help="LCS Threshold.")
    
    args = parser.parse_args()
    
    input_folder = args.ots_folder
    output_folder = args.output
    dictionary_path = args.dict
    k = args.k
    t = args.t
    
    process_files(input_folder, output_folder, dictionary_path, k, t)

if __name__ == "__main__":
    main()
