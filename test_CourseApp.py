import unittest2


class TestSourceApp(unittest2.TestCase):
    def test_format_hyperlink_no_hyperlink(self):
        from main import CourseApp
        app = CourseApp()
        self.assertEqual('Hello world', app.format_hyperlink('Hello world'))

    def test_format_hyperlink_one_hyperlink(self):
        from main import CourseApp
        app = CourseApp()
        self.assertEqual('Hello world. [ref=https://en.wikipedia.org/wiki/Unit_testing][color=#00009E]Unit testing[/color][/ref] is cool.', app.format_hyperlink(
            'Hello world. `Unit testing <https://en.wikipedia.org/wiki/Unit_testing>`_ is cool.'));

    def test_format_hyperlink_two_hyperlinks(self):
        from main import CourseApp
        app = CourseApp()
        self.assertEqual('Hello world. [ref=https://en.wikipedia.org/wiki/Unit_testing][color=#00009E]Unit testing[/color][/ref] is cool. [ref=https://docs.python.org/2/library/unittest.html][color=#00009E]Check out this link[/color][/ref] for details.',app.format_hyperlink(
            'Hello world. `Unit testing <https://en.wikipedia.org/wiki/Unit_testing>`_ is cool. `Check out this link <https://docs.python.org/2/library/unittest.html>`_ for details.'))


if __name__ == 'main':
    unittest2.main()
