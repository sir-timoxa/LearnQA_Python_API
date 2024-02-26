def test_short_phrase():
    phrase = input("Set a phrase: ")

    assert len(phrase) < 15, "Phrase is bigger or equal 15 symbols"
