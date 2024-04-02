from flask import Flask, render_template, request
import script

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        language = request.form['language']
        try:
            version = request.form['version']
        except:
            pass
        search_term = request.form['search_t']
        start_book = request.form['start_book']
        end_book = request.form['end_book']
        accuracy = request.form['accuracy']
        script.append_to_file(search_term, accuracy)
        if language == 'English':
            results = script.search_in_bible(search_term,script.count_words(search_term),accuracy)
            if results:
                results = script.filter_tuples_by_number(script.filter_results_by_books(results,script.extract_sublist(start_book,end_book,script.books)),accuracy)
            return render_template('resultsEnglish.html', results=sorted(results, key=lambda x: x[5],reverse=True), language=language)

        elif language == 'Hebrew':
            if version == 'old':
                results = script.search_in_bibleH(search_term,script.count_words(search_term),accuracy,'bibleH.txt')
                if results:
                    results = script.filter_tuples_by_number(script.filter_results_by_books(results,script.extract_sublist(start_book,end_book,script.booksH)),accuracy)
                return render_template('resultsHebrew.html', results=sorted(results, key=lambda x: x[5],reverse=True), language=language)
            elif version == 'new':
                results = script.search_in_bibleH(search_term,script.count_words(search_term),accuracy,'bibleHN.txt')
                if results:
                    results = script.filter_tuples_by_number(script.filter_results_by_books(results,script.extract_sublist(start_book,end_book,script.booksH)),accuracy)
                return render_template('resultsHebrew.html', results=sorted(results, key=lambda x: x[5],reverse=True), language=language)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)