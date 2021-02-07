from example import docstring_test


class TestDocstringTest:
    def test_docstring_test(self):
        input = None
        expected = 1
        result = docstring_test()
        assert result == expected
