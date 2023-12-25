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
        search_term = request.form['search_t']
        start_book = request.form['start_book']
        end_book = request.form['end_book']
        accuracy = request.form['accuracy']
        if language == 'English':
            results = script.check_number_and_string(search_term, accuracy)
            if results:
                results = script.filter_results_by_books(results,script.extract_sublist(start_book, end_book, script.books))
                results = sorted(results, key=lambda x: x[5] ,reverse=True)
            return render_template('resultsEnglish.html', results = results, language=language)

        elif language == 'Hebrew':
            results = script.check_number_and_string(search_term,accuracy)
            if results:
                results = script.filter_results_by_books(results,script.extract_sublist(start_book,end_book,script.booksH))
            return render_template('resultsHebrew.html', results=sorted(results, key=lambda x: x[5],reverse=True), language=language)
    return render_template('index.html')

if __name__ == '__main__':
    # script.delete_file_content(script.f)
    # print(script.read_pickle_file("hashmap_data.pkl"))
    app.run(debug=True)
