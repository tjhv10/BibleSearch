from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from bidi.algorithm import get_display
from main import search_in_bible, search_in_bibleH, booksH
from kivy.config import Config

class RTLTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        new_substring = get_display(substring)
        return super().insert_text(new_substring, from_undo=from_undo)

class BibleSearchApp(App):
    def build(self):
        try:
            hebrew_font = 'font.ttf'  # Replace with the path to your Hebrew font file

            self.results_layout = BoxLayout(orientation='vertical', spacing=1, size_hint_y=None)
            self.results_layout.bind(minimum_height=self.results_layout.setter('height'))

            self.scroll_view = ScrollView(size_hint=(1, 35), bar_width='10dp')
            self.scroll_view.add_widget(self.results_layout)

            self.search_input = RTLTextInput(
                text="",
                multiline=False,
                font_name=hebrew_font,
                size_hint_y=None,
                height=40
            )
            self.percent_input = RTLTextInput(
                text="90",
                multiline=False,
                font_name=hebrew_font,
                size_hint_y=None,
                height=40
            )

            # Store a reference to the search input
            self.search_text_input = self.search_input

            self.start_button = Button(
                text="Start Search",
                on_press=self.start_search,
                size_hint_y=None,
                height=40
            )

            # Grid layout for the input elements at the top
            input_grid = BoxLayout(orientation='horizontal')
            input_grid.add_widget(self.search_input)
            input_grid.add_widget(self.percent_input)
            input_grid.add_widget(self.start_button)

            layout = BoxLayout(orientation="vertical")
            layout.add_widget(input_grid)
            layout.add_widget(self.scroll_view)

            # Configuring Kivy for mouse events
            Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
            Config.set('input', 'mouse', 'mouse,disable_multitouch')

            return layout

        except Exception as e:
            print(f"Error: {e}")

    def start_search(self, instance):
        search_input = self.search_text_input.text
        percent = self.percent_input.text
        chosen_books = booksH
        start_book = "Genesis"
        end_book = "Revelation"

        if search_input and percent and chosen_books:
            results, count = search_in_bibleH(search_input, len(search_input.split()), percent, chosen_books)

            if results:
                self.display_results(results)
            else:
                self.results_layout.clear_widgets()
                self.results_layout.add_widget(Label(text="לא נמצאו תוצאות.", font_size='20sp'))

    def display_results(self, results):
        self.results_layout.clear_widgets()
        for result in results:
            formatted_text = f"[b]ספר:[/b] {result[0]}, [b]פרק:[/b] {result[1]}, [b]פסוק:[/b] {result[2]}\n[b]הפסוק המלא:[/b] {result[3]}"
            bidi_formatted = get_display(formatted_text)
            label = Label(text=bidi_formatted, font_name='font.ttf', markup=True, font_size='16sp', size_hint_y=None, height=100, valign='top')
            self.results_layout.add_widget(label)

if __name__ == "__main__":
    BibleSearchApp().run()
