<div align="center">    
 
## Post-OCR Correction using few/zero-shot prompting in LLM

</div>

### Abstract

This project provides a set of scripts to correct OCR output using few-shot or zero-shot learning. The main components of the project include generating word lists, creating prompts, and evaluating OCR correction results.

### Directory Trees
```
├───bali
│   ├───ann
│   ├───img
│   ├───ots
│   ├───post-ocr-correction
│   │   ├───gpt-4o_fewShot
│   │   ├───gpt-4o_zeroShot
│   │   ├───llama3-70b-instruct_fewShot
│   │   └───llama3-70b-instruct_zeroShot
│   ├───prompt-template
│   │   ├───gpt-4o_fewShot
│   │   ├───gpt-4o_zeroShot
│   │   ├───llama3-70b-instruct_fewShot
│   │   └───llama3-70b-instruct_zeroShot
│   └───wordsList
├───jawa
│   ├───ann
│   ├───img
│   ├───ots
│   ├───post-ocr-correction
│   │   ├───gpt-4o_fewShot
│   │   ├───gpt-4o_zeroShot
│   │   ├───llama3-70b-instruct_fewShot
│   │   └───llama3-70b-instruct_zeroShot
│   ├───prompt-template
│   │   ├───gpt-4o_fewShot
│   │   ├───gpt-4o_zeroShot
│   │   ├───llama3-70b-instruct_fewShot
│   │   └───llama3-70b-instruct_zeroShot
│   └───wordsList
├───minang
│   ├───ann
│   ├───img
│   ├───ots
│   ├───post-ocr-correction
│   │   ├───gpt-4o_fewShot
│   │   ├───gpt-4o_zeroShot
│   │   ├───llama3-70b-instruct_fewShot
│   │   └───llama3-70b-instruct_zeroShot
│   ├───prompt-template
│   │   ├───gpt-4o_fewShot
│   │   ├───gpt-4o_zeroShot
│   │   ├───llama3-70b-instruct_fewShot
│   │   └───llama3-70b-instruct_zeroShot
│   └───wordsList
└───sunda
    ├───ann
    ├───img
    ├───ots
    ├───post-ocr-correction
    │   ├───gpt-4o_fewShot
    │   ├───gpt-4o_zeroShot
    │   ├───llama3-70b-instruct_fewShot
    │   └───llama3-70b-instruct_zeroShot
    ├───prompt-template
    │   ├───gpt-4o_fewShot
    │   ├───gpt-4o_zeroShot
    │   ├───llama3-70b-instruct_fewShot
    │   └───llama3-70b-instruct_zeroShot
    └───wordsList
```

### Files

1. `main.py`: Generates OCR correction results.
2. `wordList_maker.py`: Creates word lists from a dictionary of similar words.
3. `prompt_maker.py`: Creates few-shot or zero-shot prompts for OCR correction.
4. `eval.py`: Evaluates the performance of OCR correction results.

### Usage

1. `main.py`: 
    - command: 
    ```
    python main.py -prompt_dir <prompt_directory> -model_name <model_name> -lang <lang> -few_shot <true/false>
    ``` 
    - arguments:
    ```
    -prompt_dir: Directory containing prompt text files.
    -model_name: Model name to use for OCR correction (e.g., meta/llama3-7b-instruct).
    -lang: Language of the text to decide the output directory (sunda, jawa, minang, or bali).
    -few_shot: True for few-shot, False for zero-shot prompting.
    ```

2. `wordList_maker.py`:
    - command:
    ```
    python wordList_maker.py -ots_folder <ocr_plain_output_folder> -output <json_examples_output_folder> -dict <dictionary_path> -k <k_value> -t <threshold>
    ```
    - arguments:
    ```
    -ots_folder: Folder containing OCR plain output text files.
    -output: Folder to save JSON examples output.
    -dict: Path to the dictionary file (Excel format).
    -k: Maximum number of similar words.
    -t: LCS threshold.
    ```

3. `prompt_maker.py`:
    - command:
    ```
    python prompt_maker.py -model_name <model_name> -word_list <word_list_folder> -input_folder <input_text_folder> -few_shot <true_or_false> -language <language>
    ```
    - arguments:
    ```
    -model_name: Hugging Face model name.
    -word_list: Folder containing JSON files with similar words.
    -input_folder: Folder containing input text files.
    -few_shot: True for few-shot, False for zero-shot prompting.
    -language: Language of the text (Sundanese, Javanese, Minangkabau, or Balinese).
    ```

4. `eval.py`:
    - command:
    ```
    python eval.py -ann <annotation_folder> -ots <ocr_plain_output_folder> -post <post_ocr_correction_folder>
    ```
    - arguments:
    ```
    -ann: Folder containing human annotation text files.
    -ots: Folder containing plain OCR text files.
    -post: Folder containing post OCR correction text files.
    ```
