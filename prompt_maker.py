import argparse
import json
import os

from datasets import load_dataset

def create_few_shot_prompt(input_text, language, examples):
    """Create a few-shot prompt for the Hugging Face model with examples and input text."""
    prompt = f"Please correct the OCR output in {language} language:\n{input_text}\n\n"
    if examples:
        examples_prompts = "To help with the ocr correction task, here is some pairs of words inside the input text and its similar words from sundanese dictionary, you can correct an ocr output by using some pairs below as a reference for OCR-Correction Task:\n"
        for example in examples:
            examples_prompts += f"{example['input']}: {example['output']}\n"
        prompt += examples_prompts
        prompt += "\n"
    prompt += "Note: The OCR output may contain incorrect text due to unclear image quality. Please remove any incorrect substrings and correct the remaining text to produce the most accurate output.\n"
    prompt += f"Desired Output: Corrected text in {language} language with proper punctuation and spacing.\nOutput:"
    return prompt

def create_zero_shot_prompt(input_text, language):
    prompt = f"Please correct the OCR output in {language} language:\n{input_text}\n"
    prompt += "Note: The OCR output may contain incorrect text due to unclear image quality. Please remove any incorrect substrings and correct the remaining text to produce the most accurate output.\n"
    prompt += f"Desired Output: Corrected text in {language} language with proper punctuation and spacing.\nOutput:"
    return prompt

def save_text(data, file_path):
    """Save data to a text file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

def load_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_text(file_path):
    """Load data from a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def main():
    parser = argparse.ArgumentParser(description="Save the prompt.")
    parser.add_argument("-model_name", type=str, required=True, help="Hugging Face model name")
    parser.add_argument("-word_list", type=str, required=True, help="Folder containing JSON files with similar words")
    parser.add_argument("-input_folder", type=str, required=True, help="Folder containing input text files")
    parser.add_argument("-few_shot", type=str, required=True, help="True for few-shot, False for zero-shot prompting")
    parser.add_argument("-language", type=str, required=True, help="Sundanese, Javanese, Minangkabau, or Bali")
    
    args = parser.parse_args()
    
    allowed_languages = ["Sundanese", "Javanese", "Minangkabau", "Balinese"]
    if args.language not in allowed_languages:
        raise ValueError(f"Invalid language: {args.language}. Must be one of {', '.join(allowed_languages)}")

    few_shot = args.few_shot.lower() == 'true'
    shot_type = "fewShot" if few_shot else "zeroShot"
    
    language = args.language
    if language == "Minangkabau":
        lang = "minang"
    elif language == "Javanese":
        lang = "jawa"
    elif language == "Balinese":
        lang = "bali"
    else:
        lang = "sunda"
    
    model_name_part = args.model_name.split('/')[-1]
    output_folder = f"{lang}/prompt-template/{model_name_part}_{shot_type}"
    os.makedirs(output_folder, exist_ok=True)

    for i in range(1, 101):
        json_path = os.path.join(args.word_list, f"{i}.json")
        text_path = os.path.join(args.input_folder, f"{i}.txt")
        output_path = os.path.join(output_folder, f"{i}.txt")

        if few_shot:
            if os.path.getsize(json_path) == 0:
                examples = []
            else:
                examples = load_dataset("json", data_files=json_path, split="train", cache_dir="./cache")
            input_text = load_text(text_path)
            prompt = create_few_shot_prompt(input_text, language, examples)
        else:
            input_text = load_text(text_path)
            prompt = create_zero_shot_prompt(input_text, language)
            
        save_text(prompt, output_path)

if __name__ == "__main__":
    main()
