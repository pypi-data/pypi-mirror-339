from pathlib import Path
import pytest
import sieve


def test_file():
    sieve_file = sieve.File("foo/bar.txt")
    assert sieve_file._path == "foo/bar.txt"
    assert sieve_file.url == None

    sieve_file = sieve.File("https://example.com/foo/bar.txt")
    assert sieve_file._path == None
    assert sieve_file.url == "https://example.com/foo/bar.txt"

    sieve_file = sieve.File(Path("foo/bar.txt"))
    assert sieve_file._path == "foo/bar.txt"
    assert sieve_file.url == None

    with pytest.raises(ValueError):
        sieve.File(
            "https://example.com/foo/bar.txt",
            url="https://example.com/foo/bar.txt",
        )


# Zight uses extra arguments in the File class, we cant break this
def test_file_extras():
    sieve_file = sieve.File("foo/bar.txt", zight="zight", alri="alri")

    assert sieve_file.__dict__ == {
        "_path": "foo/bar.txt",
        "zight": "zight",
        "alri": "alri",
        "url": None,
    }
