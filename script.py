import time
from difflib import SequenceMatcher
import pickle
import os

def is_hebrew(text):
    hebrew_range = (0x0590, 0x05FF)  # Unicode range for Hebrew characters
    return all(hebrew_range[0] <= ord(char) <= hebrew_range[1] for char in text)

# Load hashmap from file using pickle


def load_hashmap_from_file(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError) as e:
            print(f"Error loading file: {e}")
            return {}
    else:
        return {}

def read_pickle_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except pickle.UnpicklingError as e:
        print(f"Error loading pickle file: {e}")
        return None


# Save hashmap to file using pickle
def save_hashmap_to_file(filename, hashmap_data):
    with open(filename, 'wb') as file:
        pickle.dump(hashmap_data, file)


# Check number and string with hashmap
def check_number_and_string(string, number):
    hashmap = load_hashmap_from_file('hashmap_data.pkl')

    key = (string, number)

    if key in hashmap:
        return hashmap[key],hashmap[key][-1]
    else:
        if is_hebrew(string):
            hashmap[key],best_match = search_in_bibleH(string,count_words(string),number,booksH)
        else:
            hashmap[key],best_match = search_in_bible(string, count_words(string), number, books)

    save_hashmap_to_file('hashmap_data.pkl', hashmap)  # Save the updated hashmap to the file
    return hashmap[key],best_match


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
def filter_results_by_books(results, chosen_books):
    filtered_results = []
    for result in results:
        if result[0] in chosen_books:  # Check if the book is in the chosen books list
            filtered_results.append(result)
    return filtered_results
def extract_sublist(start_string, end_string,books):
    start_index = books.index(start_string) if start_string in books else -1
    end_index = books.index(end_string) if end_string in books else -1

    if start_index != -1 and end_index != -1 and start_index <= end_index:
        return books[start_index: end_index+1]
    else:
        return []
def bestMatch(string, list_of_str, current_book,current_verse):
    maxMatchWord = ''
    spm = 0
    string = string.strip(",.:-").lower()
    for word in list_of_str:
        # if word[:1].lower()==string[:1].lower(): #For faster but worst search
            sp = similarity_percentage(word.strip(",.:-").lower(), string)
            if sp > spm:
                maxMatchWord = word
                spm = sp
    return maxMatchWord, spm,current_book,current_verse
def search_in_bible(search_term, num_of_words, chosen_percent, chosen_books):
    results = []
    max_percent = 0
    max_book = ''
    max_verse = ''
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
                    matchedPart,percent, book,verse = bestMatch(search_term, verse_parts_list, current_book,verse_text)
                    if max_percent < percent:
                        max_percent = percent
                        max_verse = verse
                        max_book = book
                    if percent<int(chosen_percent):
                        continue
                    current_verse = verse_text.split()[0].split(':')[1]
                    current_chapter = verse_text.split()[0].split(':')[0]
                    words = verse_text.split()
                    results.append((current_book, current_chapter, current_verse, ' '.join(words[1:]), matchedPart))
        best_match = [max_book, max_verse, str(int(max_percent))]
        # highlight_substring('This is the verse with the highest percent of match ' + max_book + ' ' + max_verse + ' with the percent: ' + str(int(max_percent)), max_book + ' ' + max_verse)
        return results,best_match

    except FileNotFoundError:
        print("File 'bible.txt' not found.")
        return results

booksH = ['בראשית', 'שמות', 'ויקרא', 'במדבר', 'דברים', 'יהושוע', 'שופטים', 'שמואל א', 'שמואל ב', 'מלכים א', 'מלכים ב', 'ישעיה',
         'ירמיה', 'יחזקאל', 'הושע', 'יואל', 'עמוס', 'עובדיה', 'יונה', 'מיכה', 'נחום', 'חבקוק', 'צפניה', 'חגי', 'זכריה',
         'מלאכי', 'תהילים', 'משלי', 'איוב', 'שיר השירים', 'רות', 'איכה', 'קהלת', 'אסתר', 'דניאל', 'עזרא', 'נחמיה',
         'דברי הימים א', 'דברי הימים ב', 'מתי', 'מרקוס', 'לוקס', 'יוחנן', 'מעשי השליחים', 'אל הרומים', 'הראשונה אל הקורינתים',
         'השניה אל הקורינתים', 'אל הגלטים', 'אל האפסים', 'אל הפיליפים', 'אל הקולוסים', 'הראשונה אל התסלוניקים',
         'השניה אל התסלוניקים', 'הראשונה אל טימותיאוס', 'השניה אל טימותיאוס', 'אל טיטוס', 'אל פילימון', 'אל העברים', 'אגרת יעקב',
         'הראשונה לכיפא', 'השניה לכיפא', 'הראשונה ליוחנן', 'השניה ליוחנן', 'השלישית ליוחנן', 'איגרת יהודה', 'התגלות']


def search_in_bibleH(search_term, num_of_words, chosen_percent, chosen_books):
    results = []
    max_percent = 0
    max_match = ''
    max_book = ''
    max_verse = ''
    best_match = []
    try:
        with open('bibleH.txt', 'r', encoding='utf-8') as file:
            flag = False
            lines = file.readlines()
            for line in lines:
                if line.startswith('$:'):
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
                    matchedPart, percent, book, verse = bestMatch(search_term, verse_parts_list, current_book,verse_text)
                    if max_percent < percent:
                        max_percent = percent
                        max_verse = verse
                        max_book = book
                    if percent<int(chosen_percent):
                        continue
                    current_verse = verse_text.split()[0].split(':')[1]
                    current_chapter = verse_text.split()[0].split(':')[0]
                    words = verse_text.split()
                    results.append((current_book, current_chapter, current_verse, ' '.join(words[1:]), matchedPart,int(percent)))
        best_match = [max_book,max_verse,str(int(max_percent))]
        return results,best_match

    except FileNotFoundError:
        print("File 'bibleH.txt' not found.")
        return results
listt,best_match = check_number_and_string("אהבה",87)
print(best_match)
print(read_pickle_file('hashmap_data.pkl'))