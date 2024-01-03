from flask import Flask, render_template, request
import script
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        language = request.form['language']
        search_term = request.form['search_t']
        start_book = request.form['start_book']
        end_book = request.form['end_book']
        accuracy = request.form['accuracy']
        script.append_to_file(search_term, accuracy)
        if language == 'English':
            if int(accuracy)>=75:
                results = script.check_number_and_string(search_term,75)
            else:
                results = script.search_in_bible(search_term,script.count_words(search_term),accuracy,script.books)
            if results:
                results = script.filter_tuples_by_number(script.filter_results_by_books(results,script.extract_sublist(start_book,end_book,script.books)),accuracy)
            return render_template('resultsEnglish.html', results=sorted(results, key=lambda x: x[5],reverse=True), language=language)

        elif language == 'Hebrew':
            if int(accuracy)>=75:
                results = script.check_number_and_string(search_term,75)
            else:
                results = script.search_in_bibleH(search_term,script.count_words(search_term),accuracy,script.booksH)
            if results:
                results = script.filter_tuples_by_number(script.filter_results_by_books(results,script.extract_sublist(start_book,end_book,script.booksH)),accuracy)
            return render_template('resultsHebrew.html', results=sorted(results, key=lambda x: x[5],reverse=True), language=language)
    return render_template('index.html')


if __name__ == '__main__':
    # script.delete_file_content(script.f)
    # print(script.read_pickle_file("hashmap_data.pkl"))
    # script.read_pickle_file("hashmap_data.pkl")
    # web = webdriver.Chrome()
    # url = 'http://www.kirjasilta.net/hadash/Hit.1.html'
    # web.get(url)
    # for i in range(1, 29):
    #     url = 'http://www.kirjasilta.net/hadash/Hit.' + str(i) + '.html'
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     paragraphs = soup.find_all('p')
    #     with open('bibleHNf.txt', 'a', encoding='utf-8') as file:
    #         for j in range(2, len(paragraphs)):
    #             text_to_write = web.find_element(By.XPATH, '/html/body/p[' + str(j) + ']').text
    #             file.write(text_to_write + '\n')
    #     web.find_element(By.XPATH, '/html/body/p[' + str(j + 1) + ']/a[1]').click()
    app.run(debug=True)
