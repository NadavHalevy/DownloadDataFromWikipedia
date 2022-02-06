import main


def test_make_soup():
    soup = main.make_soup(main.WIKI_URL)
    table = soup.find_all('table', class_="wikitable")
    if not table:
        assert False
    assert True


def test_create_an_animal_array():
    animals_array = main.create_an_animal_array(main.table)
    for animal in animals_array:
        if animal == " ":
            assert False
    assert True
