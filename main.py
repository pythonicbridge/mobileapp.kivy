import string
import re
import urllib2
from threading import Thread

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex


class PageNode():
    def __init__(self):
        self.name = None
        self.title = None
        self.parent = None
        self.children = None
        self.next_sibling = None

    def get_next(self):
        if self.children is not None and len(self.children) > 0:
            return self.children[0]
        elif self.next_sibling is not None:
            return self.next_sibling
        elif self.parent is not None and self.parent.next_sibling is not None:
            return self.parent.next_sibling
        else:
            return None


class PageLabel(Label):
    pass


class CourseApp(App):

    def __init__(self, **kwargs):
        super(CourseApp, self).__init__(**kwargs)
        self.home_page = PageNode()
        self.home_page.name = 'index'
        self.current_page = None
        self.references = dict()
        self.programming_quiz_original_code = ''

    def load_page(self, page_name):
        self.root.ids.screen_manager.current = 'loading'
        def got_text(request, text):
            self.parse_text(text)
        request = UrlRequest(
            url='https://raw.githubusercontent.com/pythonicbridge/mobileapp.course/master/docs/{}.rst'.format(
                page_name), on_success=got_text)

    def parse_text(self, text):
        title = ''
        paragraph = ''
        menu_caption = ''
        state = ''
        state2 = ''
        code = ''
        trim_pos = -2
        line_number = 0
        children_name = list()
        for line in text.splitlines():
            line_number = line_number + 1
            if line_number == 1:
                title = line
            if line_number >= 4:
                if line_number == 4:
                    state = 'Paragraph'

                if line == '.. toctree::':
                    state = 'MenuCaption'
                elif line == '.. code:: python':
                    state = 'Code'
                    code = ''
                    continue

                if state == 'Paragraph':
                    line = self.format_hyperlink(line)
                    paragraph = paragraph + line + '\n'
                elif state == 'MenuCaption':
                    caption_attribute = ':caption:'
                    pos = string.find(line, caption_attribute)
                    if pos > -1:
                        menu_caption = (line[pos + len(caption_attribute):]).strip()
                        state = 'MenuItem'
                elif state == 'MenuItem':
                    if len(line) > 0:
                        children_name.append(line.strip())
                elif state == 'Code':
                    pos = string.find(line, '# PROGRAMMING QUIZ')
                    if pos > -1:
                        state2 = 'ProgrammingQuiz'
                        trim_pos = pos

                    if trim_pos > 0:
                        code = code + '\n' + line[trim_pos:]
                    else:
                        code = code + '\n' + line

                    if string.find(line, '# END OF PROGRAMMING QUIZ') == trim_pos:
                        if state2 == 'ProgrammingQuiz':
                            self.root.ids.code_input.text = self.programming_quiz_original_code = code
                            paragraph = paragraph + '[ref=programming_quiz][color=#00009E]Launch Programming Quiz[/color][/ref]' + '\n';
                            state = 'Paragraph'
                            state2 = ''
                            code = ''
                    elif state2 != 'ProgrammingQuiz':
                        m = re.match('[^ ]', line)
                        if m and m.start() == 0:
                            paragraph = paragraph + '.. code:: python' + code + '\n'
                            state = 'Paragraph'
                            state2 = ''
                            code = ''

        self.current_page.title = title
        self.current_page.children = list()
        self.current_page.references = dict()
        for child_name in children_name:
            page = PageNode()
            page.name = child_name
            page.title = page.name
            page.parent = self.current_page
            if len(self.current_page.children) > 0:
                previous_siberling = self.current_page.children[-1]
                previous_siberling.next_sibling = page
            self.current_page.children.append(page)
            self.references[page.name] = page

        Window.set_title(str(title))
        def update_page():
            menu_items = ''
            for page in self.current_page.children:
                menu_items = menu_items + '[ref={}][color=#00009E]{}[/color][/ref]\n'.format(page.name, page.title)
            menu = '[size=20][b]{}[/b][/size]\n\n{}'.format(menu_caption, menu_items)
            page_text = '[size=30][b]{}[/b][/size]\n\n{}\n{}'.format(title, paragraph, menu)
            self.root.ids.page_label.text = page_text
            self.root.ids.screen_manager.current = 'page'

        def get_menu(arg):
            for page in self.current_page.children:
                if len(page.name) > 0:
                    response = urllib2.urlopen(url='https://raw.githubusercontent.com/pythonicbridge/mobileapp.course/master/docs/{}.rst'.format(page.name))
                    text = response.read()
                    for line in text.splitlines():
                        page.title = line
                        break
            def got_menu(dt):
                update_page()
            Clock.schedule_once(got_menu)

        thread = Thread(target=get_menu, args=(None,))
        thread.start()

    def format_hyperlink(self, line):
        # return line # attempt 1: this will pass 1 test
        # return re.sub('`(.*) <([^>]*)>`_', r'[ref=\2]\1[/ref]', line) # attempt 2: this will pass 2 tests
        return re.sub('`([^`]*) <([^>]*)>`_', r'[ref=\2][color=#00009E]\1[/color][/ref]', line) # attempt 3: this will pass all tests

    def on_page_label_ref_press(self, instance, value):
        page = self.references.get(value, None)
        if page is not None:
            self.current_page = page
            self.load_page(page_name=self.current_page.name)
        elif string.find(value, 'http') == 0:
            if __name__ != '__android__':
                import webbrowser
                webbrowser.open(value);
        elif value == 'programming_quiz':
            self.root.ids.screen_manager.current = 'programming_quiz'

    def on_programming_quiz_run_test(self, arg):
        import code
        run="""
runner = unittest2.TextTestRunner(stream=context['mystream'])
suite = unittest2.TestSuite()
suite.addTest(unittest2.makeSuite(ProgrammingQuiz))
context['test'] = runner.run(suite)
        """
        co = code.compile_command(self.root.ids.code_input.text + '\n{}'.format(run), "<stdin>", "exec")
        if co:
            from cStringIO import StringIO
            mystream = StringIO()
            context = dict()
            context['mystream'] = mystream
            exec(co, dict(globals(), context=context))
            self.root.ids.code_output.text = str(context['test']) + '\n' + context['mystream'].getvalue()

    def on_programming_quiz_reset(self, arg):
        self.root.ids.code_input.text = self.programming_quiz_original_code

    def on_programming_quiz_move_on(self, arg):
        self.on_next()

    def on_start(self):
        self.on_home()

    def on_home(self):
        self.current_page = self.home_page
        self.load_page(page_name=self.current_page.name)

    def on_next(self):
        next_page = self.current_page.get_next()
        if next_page is not None:
            self.current_page = next_page
            self.load_page(page_name=self.current_page.name)

    def on_up(self):
        up_page = self.current_page.parent
        if up_page is not None:
            self.current_page = up_page
            self.load_page(page_name=self.current_page.name)

def main():
    Window.clearcolor = get_color_from_hex('#FFFFFF')
    CourseApp().run()


if __name__ in ('__main__', '__android__'):
    main()
