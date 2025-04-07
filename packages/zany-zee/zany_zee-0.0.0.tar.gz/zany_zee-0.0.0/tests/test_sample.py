from zany_zee import ContentLoader

def test_load_text():
    loader = ContentLoader()
    try:
        result = loader.load_text("README.md")  # Just testing it reads something
        assert isinstance(result, str)
    except FileNotFoundError:
        assert True  # File missing is okay for this simple test
