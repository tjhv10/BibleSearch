import re

def find_chapter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        matches = re.findall(r'([\u0590-\u05FF]+) {2}', text)
        return matches


def find_book(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        matches = re.findall(r'\$:([\u0590-\u05FF]+(?: [\u0590-\u05FF]+)*)', text)
        return matches

file_path = 'bibleH.txt'
print( find_book(file_path))


  # Replace this with the path to your text file
hebrew_words_with_two_spaces = find_chapter(file_path)
print("Hebrew words with two spaces after them:", hebrew_words_with_two_spaces)
