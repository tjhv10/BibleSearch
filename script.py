from difflib import SequenceMatcher
from datetime import datetime,timedelta
import socket
import json

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
    # print(results)
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
def search_in_bible(search_term, num_of_words, chosen_percent):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 9998))
        # Send a message to the server
        send_message(sock,json.dumps(search_term+"@"+str(num_of_words)+"@"+str(chosen_percent)+"@bible.txt"))
        # Receive and print the server's response
        response = receive_message(sock)
    result = response.split("\r\n")[:-1]
    tResult = []
    for res in result:
            tResult.append(res.split('@'))
    result = tResult
    for res in result:
        res[5] = int(float(res[5]))
        # print(res)
    return result

booksH = ['בראשית', 'שמות', 'ויקרא', 'במדבר', 'דברים', 'יהושוע', 'שופטים', 'שמואל א', 'שמואל ב', 'מלכים א', 'מלכים ב', 'ישעיה',
         'ירמיה', 'יחזקאל', 'הושע', 'יואל', 'עמוס', 'עובדיה', 'יונה', 'מיכה', 'נחום', 'חבקוק', 'צפניה', 'חגי', 'זכריה',
         'מלאכי', 'תהילים', 'משלי', 'איוב', 'שיר השירים', 'רות', 'איכה', 'קהלת', 'אסתר', 'דניאל', 'עזרא', 'נחמיה',
         'דברי הימים א', 'דברי הימים ב', 'מתי', 'מרקוס', 'לוקס', 'יוחנן', 'מעשי השליחים', 'אל הרומים', 'הראשונה אל הקורינתים',
         'השניה אל הקורינתים', 'אל הגלטים', 'אל האפסים', 'אל הפיליפים', 'אל הקולוסים', 'הראשונה אל התסלוניקים',
         'השניה אל התסלוניקים', 'הראשונה אל טימותיאוס', 'השניה אל טימותיאוס', 'אל טיטוס', 'אל פילימון', 'אל העברים', 'אגרת יעקב',
         'הראשונה לכיפא', 'השניה לכיפא', 'הראשונה ליוחנן', 'השניה ליוחנן', 'השלישית ליוחנן', 'איגרת יהודה', 'התגלות']

def send_message(sock, message):
    message += '\n'  # Append newline character
    sock.sendall(message.encode('utf-8'))

def receive_message(sock):
    received_data = b""
    chunk = ''
    while chunk[-5:]!=b"EOF\r\n":
        chunk = sock.recv(1024)
        if not chunk:
            break
        received_data += chunk
    received_data = received_data[:-5]
    return received_data.decode('iso-8859-8')

def search_in_bibleH(search_term, num_of_words, chosen_percent,f):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 9998))
        # Send a message to the server
        send_message(sock,json.dumps(search_term+"@"+str(num_of_words)+"@"+str(chosen_percent)+"@"+f))
        # Receive and print the server's response
        response = receive_message(sock)
    result = response.split("\r\n")[:-1]
    tResult = []
    for res in result:
            tResult.append(res.split('@'))
    result = tResult
    print(result)
    for res in result:
        res[5] = int(float(res[5]))
        # print(res)
    return result


def append_to_file(string, number):
    with open('searches.txt', 'a') as file:
        good_time = datetime.now()+timedelta(hours=2)
        good_time = good_time.strftime("%d.%m.%Y %H:%M")
        file.write(f"{string} {number} {good_time}\n")

def filter_tuples_by_number(lst, num):
        filtered_list = []
        for item in lst:
            if int(item[-1]) >= int(num):
                filtered_list.append(item)
        return filtered_list
print(search_in_bible("gray",1,75))