
from difflib import SequenceMatcher

books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
    '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm', 'Proverbs',
    'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
    'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew',
    'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians',
    'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
    'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']


def similarity_percentage(string1, string2):
    return 100 * SequenceMatcher(None, string1, string2).ratio()


def count_words(line):
    return len(line.split())


def combine_lists_as_strings(list_of_lists):
    combined_list = []
    for inner_list in list_of_lists:
        combined_list.append(' '.join(inner_list))
    return combined_list


def create_word_groups(num_of_words_in_each_group, text):
    words = text.split()
    word_groups = []

    for i in range(0, len(words)-num_of_words_in_each_group+1):
        word_groups.append(words[i:i + num_of_words_in_each_group])

    return combine_lists_as_strings(word_groups)


def bestMatch(string, list_of_str, percent_of_accuracy):
    maxMatchWord = ''
    spm = 0
    string = string.strip(",.:").lower()
    for word in list_of_str:
        sp = similarity_percentage(word.strip(",.:").lower(), string)
        if sp > spm:
            if sp >= int(percent_of_accuracy):
                maxMatchWord = word
                spm = sp
    return maxMatchWord


def highlight_substring(main_string, substring):
    start_index = main_string.find(substring)

    if start_index != -1:
        end_index = start_index + len(substring.strip(",.:;"))
        highlighted_string = (
                main_string[:start_index]
                + "\033[93m" + main_string[start_index:end_index]
                + "\033[0m"
                + main_string[end_index:]
        )
        print("Full Verse: " + highlighted_string)
    else:
        print("Full Verse: " + main_string)


def extract_sublist(start_string, end_string):
    start_index = books.index(start_string) if start_string in books else -1
    end_index = books.index(end_string) if end_string in books else -1

    if start_index != -1 and end_index != -1 and start_index <= end_index:
        return books[start_index: end_index+1]
    else:
        return []


def search_in_bible(search_term, num_of_words, chosen_percent, chosen_books):
    results = []
    try:
        with open("bible.txt", 'r') as file:
            flag = False
            lines = file.readlines()
            for line in lines:
                if line.startswith('T:'):
                    current_book = line.split(':')[1].strip()
                    if current_book not in chosen_books:
                        flag = False
                        continue
                    else:
                        flag = True
                else:
                    if not flag:
                        continue
                    verse_text = line.strip()
                    verse_parts_list = create_word_groups(num_of_words, verse_text)
                    matchedPart = bestMatch(search_term, verse_parts_list, chosen_percent)
                    if matchedPart == '':
                        continue
                    current_verse = verse_text.split()[0].split(':')[1]
                    current_chapter = verse_text.split()[0].split(':')[0]
                    words = verse_text.split()
                    results.append((current_book, current_chapter, current_verse, ' '.join(words[1:]), matchedPart))

        return results

    except FileNotFoundError:
        print("File 'bible.txt' not found.")
        return results


search_input = input("Enter the word, part of a verse, or a full verse to search for: ")
percent = input("Enter the percentage of accuracy to search for (90% is recommended): ")
print("\033[93mHere is the list of the books in the bible: \033[0m")
part_length = len(books) // 3
split_parts = [books[i:i + part_length] for i in range(0, len(books), part_length)]
for part in split_parts:
    print(', '.join(part))
start_book = input("Enter the book that you want to start to search from: ")
while start_book not in books:
    start_book = input("This book is not in the books list, try again: ")
end_book = input("Enter the book that you want to end your search: ")
while end_book not in books:
    end_book = input("This book is not in the books list, try again: ")
search_results = search_in_bible(search_input, count_words(search_input), percent, extract_sublist(start_book, end_book))
if search_results:
    print(f"Results for '{search_input}':")
    for result in search_results:
        print(f"Book: {result[0]}, Chapter: {result[1]}, Verse: {result[2]}")
        highlight_substring(result[3], result[4])
else:
    print(f"No results found for '{search_input}' in the part of the bible that you chosen.")
