import re

import script


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
def split_numbers_to_rows(file_path):
    # Read the file using UTF-8 encoding for Hebrew text
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Function to split numbers with their text
        def split_numbers(line):
            # Using regular expression to find numbers and text after them
            pattern = r'(\d+)([^0-9]*)'
            parts = re.findall(pattern, line)

            # Writing each number with its text in a new row
            with open(file_path, 'a', encoding='utf-8') as file:
                for number, text in parts:
                    file.write(f"{number}{text}\n")

        # Apply the split_numbers function to each line
        for line in lines:
            split_numbers(line)
def add_number_to_chapters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

        # Find chapters without the first word
        matches = re.findall(r'\b([\u0590-\u05FF]+(?: {1,}[\u0590-\u05FF]+)+)\b', text)

        # Adding '1' with appropriate spacing to each chapter
        for chapter in matches:
            modified_chapter = re.sub(r'\b([\u0590-\u05FF]+)\b', r'\1 1', chapter, count=1)
            text = text.replace(chapter, f'{modified_chapter}', 1)

    # Write modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
def print_number_string_pairs(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        text = file.read()

        # Find number followed by string using regular expressions
        matches = re.findall(r'(\d+)([\s\u0590-\u05FF()]+)(?=\d+|$)', text)
        finish_string =''
        for match in matches:
            number, string_between = match
            string_between = string_between.strip()
            if string_between:  # Check if the string is not empty (ignoring spaces)
                finish_string += f"{number}:{string_between}\n"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(finish_string)
def remove_empty_lines(file_name):
    with open(file_name, 'r+',encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate(0)
        non_empty_lines = [line for line in lines if line.strip()]
        file.writelines(non_empty_lines)
def hebrew_to_gematria(hebrew_text):
    gematria_values = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
        'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
        'יא': 11, 'יב': 12, 'יג': 13, 'יד': 14, 'טו': 15,
        'טז': 16, 'יז': 17, 'יח': 18, 'יט': 19, 'כ': 20,
        'כא': 21, 'כב': 22, 'כג': 23, 'כד': 24, 'כה': 25,
        'כו': 26, 'כז': 27, 'כח': 28, 'כט': 29
    }

    numerical_values = []
    i = 0
    while i < len(hebrew_text):
        if i + 1 < len(hebrew_text) and hebrew_text[i:i+2] in gematria_values:
            numerical_values.append(gematria_values[hebrew_text[i:i+2]])
            i += 2
        else:
            numerical_values.append(gematria_values.get(hebrew_text[i], 0))
            i += 1

    return numerical_values[0]

def add_episode_to_line(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        current_episode = ''
        modified_lines = []

        for line in lines:
            line = line.strip()
            if line.isnumeric():
                current_episode = line
            else:
                modified_lines.append(f"{current_episode}:{line}")

        file.seek(0)
        file.truncate()
        file.write('\n'.join(modified_lines))
def remove_short_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    filtered_lines = [line.strip() for line in lines if len(line.strip()) >= 4]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(filtered_lines))
def add_number_to_file(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        file.seek(0, 0)  # Move the cursor to the beginning of the file
        file.write('1\n' + content)
def delete_rows_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines = lines[1:-6]  # Remove the first row and the last six rows

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(lines))
def remove_vocalization_marks(input_text):
    # Define the vocalization marks to be removed
    vocalization_marks = "ְֱֲֳִֵֶַָׇֹֺֻּֽֿׁׂׅׄ׈׉׊׋׌׍׎׼׽׾׿"

    # Remove the vocalization marks using regular expression
    cleaned_text = re.sub(f"[{vocalization_marks}]", '', input_text)
    return cleaned_text
def remove_vocalization_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = remove_vocalization_marks(text)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"Vocalization marks removed from '{file_path}' successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
def get_strings_with_marker(file_path):
    result_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                    if line.startswith("$:"):
                        result_list.append(line.split(':')[1].strip())

        return result_list
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return result_list
def add_space_around_hyphen(input_string):
    spaced_string = ' '.join(input_string.split('־'))  # Replace '־' with the Hebrew hyphen character
    return ' ' + spaced_string + ' '
def process_file_to_add_space_around_hyphen(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    modified_content = add_space_around_hyphen(content)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(modified_content)
def remove_first_rows(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        lines = file.readlines()

    # Remove the specified number of rows
    remaining_lines = lines[30775:]

    with open(file_path, 'w',encoding='utf-8') as file:
        file.writelines(remaining_lines)
def replace_pattern_in_file(file_name):
    def replace_pattern(text):
        pattern = r'(\d+:\d+):(\w+)'
        replaced_text = re.sub(pattern, r'\1 \2', text)
        return replaced_text

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = [replace_pattern(line) for line in lines]

    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
def remove_last_colon(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.rstrip().endswith('׃'):
                line = line.rstrip()[:-1] + '\n'
            file.write(line)
def is_new_testament_book_hebrew(line):
    new_testament_books_hebrew = [
        "מתי", "מרקוס", "לוקס", "יוחנן", "מעשי השליחים",
        "אל הרומים", "הראשונה אל הקורינתים", "השנייה אל הקורינתים", "אל הגלטים",
        "אל האפסים", "אל הפיליפים", "אל הקולוסים", "הראשונה אל התסלוניקים", "השנייה אל התסלוניקים",
        "הראשונה אל טימותיאוס","השנייה אל טימותיאוס","אל טיטוס",
        "אל פילימון", "אל העברים", "אגרת יעקב", "הראשונה של כיפא", "השנייה של כיפא","הראשונה של יוחנן","השנייה של יוחנן"
        ,"השלישית של יוחנן","אגרת יהודה","התגלות"
    ]

    for book in new_testament_books_hebrew:
        if book in line:
            return True
    return False
def add_marker_to_new_testament_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if is_new_testament_book_hebrew(line) and not any(char.isdigit() for char in line):
            updated_lines.append("$:" + line)
            print(line)
        else:
            updated_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)
def remove_marker(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = [line.replace("$:", "") for line in lines]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)
def has_vocalization_marks(text):
    # Regular expression to match Hebrew vocalization marks (nikkud)
    vocalization_marks = "ְֱֲֳִֵֶַָׇֹֺֻּֽֿׁׂׅׄ׈׉׊׋׌׍׎׼׽׾׿"

    return any(char in text for char in vocalization_marks)
def remove_lines_without_vocalization_except_marked(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if "$:" in line or has_vocalization_marks(line):
            updated_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

def modify_file_with_gematria(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        words = line.split()
        if words and '$:' in words[0]:
            last_word = words[-1]
            print(last_word)
            gematria_values = hebrew_to_gematria(last_word)
            print(gematria_values)
            words[-1] = str(gematria_values)
            updated_lines.append(' '.join(words) + '\n')
        else:
            updated_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)
def split_rows_with_numbers(file_path):
    def is_number(s):
        return s.strip().isdigit()

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    previous_parts = []
    for line in lines:
        if '$' not in line:
            parts = re.split(r'(\d+)', line.strip())
            parts = [x for x in parts if x != ""]# Split on numbers
            print(parts)
            new_parts = []
            flag = False
            for part in parts:
                if part.strip():
                    if is_number(part):
                        if previous_parts:
                            flag = True

                        updated_lines.append(part.strip())
                        if flag:
                            updated_lines.append(''.join(previous_parts).strip())
                        previous_parts = new_parts = []
                        flag = False
                    else:
                        new_parts.append(part.strip())
            previous_parts += new_parts
        else:
            updated_lines.append(line.strip() + '\n')
            previous_parts = []

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_lines))
def process_file(file_path):
    def process_lines(lines):
        updated_lines = []
        has_dollar = False

        for line in lines:
            if '$' in line:
                if updated_lines and has_dollar:
                    updated_lines[-1] = updated_lines[-1].rstrip() + '\n'
                updated_lines.append(line.strip() + '\n')
                has_dollar = True
            else:
                updated_lines.append(line.strip())

        return updated_lines

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = process_lines(lines)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(updated_lines))


def add_number_to_single_letter_words(file_path):
    # Read text from file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Regular expression to find words with a single Hebrew character
    pattern = r'\b([\u0590-\u05FF])\b'

    # Find all matches
    matches = re.finditer(pattern, text)

    # Iterate through matches and modify the text
    offset = 0
    for match in matches:
        start_idx = match.start() + offset
        end_idx = match.end() + offset
        single_letter = match.group(1)

        # Add '1' to the right of the single-letter word
        text = text[:start_idx] + single_letter + '\n' + text[end_idx:]

        # Update offset for changes in text length
        offset += 1  # Additional length due to adding '1 ' to the text

    # Write modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def remove_specific_char(file_path, char_to_remove):
    # Read text from file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Remove the specified character from the text
    modified_text = text.replace(char_to_remove, '')

    # Write modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_text)
def find_and_print_single_char_words(file_path):
    # Read text from file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Regular expression to find words with a single character
    pattern = r'\b([\u0590-\u05FF])\b'

    # Find all matches
    single_char_words = re.findall(pattern, text)

    # Print single character words
    print("\n".join(single_char_words))

def add_1_to_specific_word(file_path):
    # Read text from file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Regular expression pattern to find the specific word יא
    pattern = r'\b(כז)\b'

    # Find all matches of the specific word יא
    matches = re.finditer(pattern, text)

    # Modify text by adding ' 1' after יא
    offset = 0
    for match in matches:
        start_idx = match.start() + offset
        end_idx = match.end() + offset

        # Add ' 1' after יא
        text = text[:end_idx] + '\n 1' + text[end_idx:]

        # Update offset for changes in text length
        offset += 3  # Additional length due to adding ' 1' to the text

    # Write modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def convert_hebrew_to_gematria_in_file(file_name):
    with open(file_name, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate(0)

        for line in lines:
            if len(line) < 5:
                modified_line = hebrew_to_gematria(line)
                print(modified_line)
                file.write(str(modified_line) + '\n')
            else:
                file.write(line)

def add_episodes_to_versus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    current_number = None

    for line in lines:
        words = line.strip().split()
        if len(words) == 1 and words[0].isdigit():
            current_number = words[0]
            output_lines.append(line.strip())
        elif current_number is not None and len(words) > 0:
            updated_line = ' '.join(str(current_number +':'+ word) if word.isdigit() else word for word in words)
            output_lines.append(updated_line)
        else:
            output_lines.append(line.strip())

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(output_lines))


def extract_text_with_pattern(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        words = line.strip().split()
        previous_end = 0

        for word in words:
            if '$' not in word:
                match = re.search(r'(.+?)\s*:\s*\d+', word)
                if match:
                    extracted_text = match.string
                    print(match.span())
                    match_start, match_end = match.span()
                    if match_start > 0:
                        print(f"previus end:{previous_end}")
                        print(f"match start:{match_start}")
                        between_text = word[previous_end:match_start]
                    else:
                        between_text = ""

                    print(f"Matched Text: {extracted_text}")
                    print(f"Text Between: {between_text}")

                    previous_end = match_end + 1 if match_end < len(word) else 0

def separate_lines_with_pattern(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    separated_text = re.sub(r'(\d+:\d+)\s+', r'\n\1 ', text)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(separated_text)

# Example usage:
f = 'bibleHN.txt'
def copy_rows_to_another_file(source_file, destination_file):
    with open(source_file, 'r', encoding='utf-8') as source:
        content = source.readlines()

    rows_to_write = content[:23252]

    with open(destination_file, 'r+', encoding='utf-8') as dest:
        original_content = dest.readlines()
        dest.seek(0)
        for row in rows_to_write + original_content:
            dest.write(row)
def find_identical_lines(file_path):
    lines_seen = set()
    duplicate_lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if line in lines_seen:
            duplicate_lines.append(line.strip())
        else:
            lines_seen.add(line)

    if duplicate_lines:
        print("Identical lines found:")
        for duplicate in set(duplicate_lines):
            print(duplicate)
    else:
        print("No identical lines found.")
def append_lines_without_numbers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    previous_line = ''

    for line in lines:
        if not any(char.isdigit() or char == '$' for char in line):
            previous_line += line.strip()
        else:
            if previous_line:
                updated_lines.append(previous_line)
            previous_line = line.strip()

    # Append the last line
    if previous_line:
        updated_lines.append(previous_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_lines))
def check_multiple_digit_words(file_path):
    count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):
        words_with_digits = re.findall(r'\b\w*\d\w*\b', line)
        if len(words_with_digits) > 1:
            count +=1
    print(count)
def compare_numbers_in_patterns(file_path1, file_path2):
    with open(file_path1, 'r', encoding='utf-8') as file1:
        lines1 = file1.readlines()

    with open(file_path2, 'r', encoding='utf-8') as file2:
        lines2 = file2.readlines()

    pattern = r'(\d+:\d+)'

    numbers_lines1 = [re.findall(pattern, line) for line in lines1]
    numbers_lines2 = [re.findall(pattern, line) for line in lines2]

    min_len = min(len(numbers_lines1), len(numbers_lines2))

    diff_line = min_len
    for i in range(min_len):
        if numbers_lines1[i] != numbers_lines2[i]:
            diff_line = i
            break

    if diff_line == min_len:
        print("The numbers in the patterns are the same in both files.")
    else:
        print(f"The patterns start differing at line number: {diff_line + 1}")
        print(f"File 1: {numbers_lines1[diff_line]}")
        print(f"File 2: {numbers_lines2[diff_line]}")
