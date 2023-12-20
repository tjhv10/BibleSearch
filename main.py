import time
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
        highlight_substring('This is the verse with the highest percent of match ' + max_book + ' ' + max_verse + ' with the percent: ' + str(int(max_percent)), max_book + ' ' + max_verse)
        return results,len(results)

    except FileNotFoundError:
        print("File 'bible.txt' not found.")
        return results

def search_in_English():
    search_input = input("Enter the word, part of a verse, or a full verse to search for: ")
    percent = input("Enter the percentage of accuracy to search for (90% is recommended): ")
    print("\033[93mHere is the list of the books in the bible: \033[0m")
    part_length = len(books) // 3
    split_parts = [books[i:i + part_length] for i in range(0, len(books), part_length)]
    for part in split_parts:
        print(', '.join(part))
    start_book = input("Enter the book that you want to start to search from. If you want the whole bible enter all. "
                       "If you want the old testament enter ot and if you want the new testament enter nt: ")
    end_book = ''
    flag = False
    if start_book == 'all':
        start_book = 'Genesis'
        end_book = 'Revelation'
        flag = True
    if start_book == 'ot':
        start_book = 'Genesis'
        end_book = 'Malachi'
        flag = True
    if start_book == 'nt':
        start_book = 'Matthew'
        end_book = 'Revelation'
        flag = True
    if not flag:
        while start_book not in books:
            start_book = input("This book is not in the books list, try again: ")
        end_book = input("Enter the book that you want to end your search: ")
        while end_book not in books:
            end_book = input("This book is not in the books list, try again: ")
    start_time = time.time()
    search_results,count = search_in_bible(search_input, count_words(search_input), percent, extract_sublist(start_book, end_book,books))
    end_time = time.time()
    print("Time took to search is: " + str(end_time - start_time) + " seconds")
    if search_results:
        print(str(count) + " results came back")
        print(f"Results for '{search_input}':")
        for result in search_results:
            print(f"Book: {result[0]}, Chapter: {result[1]}, Verse: {result[2]}")
            highlight_substring(result[3], result[4])

    else:
        print(f"No results found for '{search_input}' in the part of the bible that you chosen.")

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
    try:
        with open("bibleH.txt", 'r',encoding='utf-8') as file:
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
                    results.append((current_book, current_chapter, current_verse, ' '.join(words[1:]), matchedPart))
        highlight_substringH('זהו הפסוק עם ההתאמה הטובה ביותר: '+max_book+' '+max_verse + ' עם האחוזים: '+ str(int(max_percent)),max_book+' '+max_verse)
        return results,len(results)

    except FileNotFoundError:
        print("File 'bibleH.txt' not found.")
        return results

def highlight_substringH(main_string, substring):
    start_index = main_string.find(substring)

    if start_index != -1:
        end_index = start_index + len(substring.strip(",.:;-"))
        highlighted_string = (
                main_string[:start_index]
                + "\033[93m" + main_string[start_index:end_index]
                + "\033[0m"
                + main_string[end_index:]
        )
        print("פסוק: " + highlighted_string)
    else:
        print("פסוק: " + main_string)

def search_in_Hebrew():
    flag = False
    search_input = input("הכנס פסוק, חלק מפסוק או מילה: ")
    percent = input("הכנס אחוזי דיוק (90% הכי מומלץ): ")
    print("\033[93mהנה רשימה של ספרי התנך:\033[0m")
    part_length = len(booksH) // 4
    split_parts = [booksH[i:i + part_length] for i in range(0, len(booksH), part_length)]
    for part in split_parts:
        print(', '.join(part))
    start_book = input("הכנס ספר שאתה רוצה להתחיל לחפש ממנו. אם אתה רוצה את כל הכתובים הכנס הכל."
                       " אם אתה רוצה את כל התנך הכנס תנך. אם אתה רוצה את כל הברית החדשה הכנס בח: ")
    end_book = ''
    if start_book =='הכל':
        start_book = 'בראשית'
        end_book = 'התגלות'
        flag = True
    if start_book =='תנך':
        start_book = 'בראשית'
        end_book = 'דברי הימים ב'
        flag = True
    if start_book =='בח':
        start_book = 'מתי'
        end_book = 'התגלות'
        flag = True
    if not flag:
        while start_book not in booksH:
            start_book = input("הספר לא קיים, נסה שוב: ")
        end_book = input("הכנס ספר שאתה רוצה לסיים לחפש אחריו: ")
        while end_book not in booksH:
            end_book = input("הספר לא קיים, נסה שוב: ")
    start_time = time.time()
    search_results,count = search_in_bibleH(search_input, count_words(search_input), percent,extract_sublist(start_book, end_book,booksH))
    end_time = time.time()
    print("הזמן שלקח לחפש הוא: " + str(end_time - start_time) + " שניות")
    if search_results:
        print(str(count) + " תוצאות חזרו")
        print(f'תוצאות בשביל "{search_input}" בחלק של הכתובים שבחרת')
        for result in search_results:
            print(f"ספר: {result[0]}, פרק: {result[1]}, פסוק: {result[2]}")
            highlight_substringH(result[3], result[4])
    else:
        print(f'אין תוצאות בשביל "{search_input}" בחלק של הכתובים שבחרת. מומלץ להוריד את אחוזי הדיוק ולנסות שוב.')
# while 1:
#     flag = False
#     lang = input("האם אתה רוצה לחפש בעברית או אנגלית? בשביל עברית הכנס ע ובשביל אנגלית הכנס e. אם ברצונך לסיים הכנס ס: ")
#     if lang =='ע':
#         search_in_Hebrew()
#         flag = True
#     if lang == 'e':
#         search_in_English()
#         flag = True
#     if lang == 'ס':
#         break
#     if not flag:
#         input("לא בחרת שפה נכונה, לחץ אנטר ונסה שוב")