import re

def remove_tashkeel_and_numbers(text):
    # Define the pattern to match Arabic diacritics and numbers
    tashkeel_pattern = r'[\u0617-\u061A\u064B-\u0652]'  # Arabic diacritics
    numbers_pattern = r'[0-9\u0660-\u0669]'  # Arabic and English numbers
    # Remove diacritics and numbers using the regex patterns
    text = re.sub(tashkeel_pattern, '', text)
    text = re.sub(numbers_pattern, '', text)
    return text

# Read the original text from a file
with open("كتاب النحو الواضح في قواعد اللغة العربية.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Clean the text by removing diacritics and numbers
cleaned_text = remove_tashkeel_and_numbers(text)

# Write the cleaned text to a new file
with open("text_files/كتاب النحو الواضح في قواعد اللغة العربية.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Text has been cleaned by removing diacritics and numbers, and saved to 'text_files/كتاب النحو الواضح في قواعد اللغة العربية.txt'")
