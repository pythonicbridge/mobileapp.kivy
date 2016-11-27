import unittest2


class TestGistController(unittest2.TestCase):
    def test_save(self):
        from main import GistController
        controller = GistController()
        token = '70711205b0480aeee51943799bb81fde758b7375'
        gist = {
            "description":"Created via API",
            "public":"true",
            "files": {"file1.txt": {"content": "Demo"}}
        }
        result = controller.save(token, gist)
        print str(result)


if __name__ == 'main':
    unittest2.main()
