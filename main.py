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
        search_term = request.form['search_term']
        start_book = request.form['start_book']
        end_book = request.form['end_book']
        accuracy = request.form['accuracy']
        if language == 'English':
            results,best_match = script.search_in_bible(search_term, script.count_words(search_term), accuracy, script.extract_sublist(start_book,end_book,script.books))
            return render_template('resultsEnglish.html', results=results, best_match=best_match, language=language)
        elif language == 'Hebrew':
            results,best_match = script.search_in_bibleH(search_term, script.count_words(search_term), accuracy,script.extract_sublist(start_book,end_book,script.booksH) )
            return render_template('resultsHebrew.html', results=results, best_match=best_match, language=language)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
