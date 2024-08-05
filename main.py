import os
import json
import argparse

from openai import OpenAI
from datasets import load_dataset
from dotenv import load_dotenv

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Function to load text from a file
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to save text to a file
def save_text(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

# Function to load examples from a JSON file
def load_examples(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    parser = argparse.ArgumentParser(description="Get few shot or zero shot result.")
    parser.add_argument("-prompt_dir", type=str, required=True, help="Prompt directory")
    parser.add_argument("-model_name", type=str, required=True, help="Model name to use for OCR Correction")
    parser.add_argument("-lang", type=str, required=True, help="sunda, jawa, minang, or bali")
    parser.add_argument("-few_shot", type=str, required=True, help="True for few-shot, False for zero-shot prompting")
    
    args = parser.parse_args()

    allowed_languages = ["sunda", "jawa", "minang", "bali"]
    if args.lang not in allowed_languages:
        raise ValueError(f"Invalid language: {args.lang}. Must be one of {', '.join(allowed_languages)}")

    few_shot = args.few_shot.lower() == 'true'
    shot_type = "fewShot" if few_shot else "zeroShot"

    input_directory = args.prompt_dir
    model_name = args.model_name
    model_name_part = args.model_name.split('/')[-1]
    output_directory = f"{args.lang}/post-ocr-correction/{model_name_part}_{shot_type}"

    os.makedirs(output_directory, exist_ok=True)

    # Process each file
    for i in range(1, 101):
        input_file_path = os.path.join(input_directory, f"{i}.txt")
        output_file_path = os.path.join(output_directory, f"{i}.txt")
        
        # Load input text
        prompt = load_text(input_file_path)
        
        # Generate OCR correction output using OpenAI API
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )
        
        # Collect the output text
        output_text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                output_text += chunk.choices[0].delta.content
        
        # Save the output text to a file
        save_text(output_text, output_file_path)
        print(f"Generating {i} file...")

    print("Processing completed.")


if __name__ == "__main__":
    main()