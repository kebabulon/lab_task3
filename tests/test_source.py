import pytest

from src.source import Source, GeneratorSource, JsonSource, ApiSource


def test_source_protocol():
    assert isinstance(GeneratorSource(), Source)
    assert isinstance(JsonSource("example_tasks.json"), Source)
    assert isinstance(ApiSource(1), Source)


def test_json_source():
    with pytest.raises(NameError):
        json_source = JsonSource("tests/this_file_doesnt_exists.json")

    json_source = JsonSource("tests/bad_json_example.json")
    with pytest.raises(ValueError):
        json_source.get_tasks()
