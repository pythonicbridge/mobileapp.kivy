import unittest2


class TestGistController(unittest2.TestCase):
    def test_save(self):
        from main import GistController
        controller = GistController()
        token = 'bc754134ec6bbd3d75ecfbc50ce3f96ff69103ad'[::-1] # Token for Public Demo Acount. To be externalized
        gist = {
            "description":"Created via API",
            "public":"true",
            "files": {"file1.txt": {"content": "Demo"}}
        }
        result = controller.save(token, gist)
        print str(result)


if __name__ == 'main':
    unittest2.main()
