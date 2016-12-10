import unittest2


class TestGistController(unittest2.TestCase):
    def test_save(self):
        from main import GistController
        controller = GistController()
        token = '13b144c43b1d98974ce32a8e492f43ce1b523ca8' # Token for Public Demo Acount. To be externalized
        gist = {
            "description":"Created via API",
            "public":"true",
            "files": {"file1.txt": {"content": "Demo"}}
        }
        result = controller.save(token, gist)
        print str(result)


if __name__ == 'main':
    unittest2.main()
