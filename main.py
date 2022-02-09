from bs4 import BeautifulSoup
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"


def make_soup(url):
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, "html.parser")
    return soup_data


def create_a_collateral_adjective_list(table_data):
    collateral_adjective_saved = " "
    for record in table_data.findAll('tr'):
        collateral_adjective = ""
        for data in record.findAll('td')[5:6]:
            collateral_adjective = collateral_adjective + "," + data.text
        collateral_adjective_saved = collateral_adjective_saved + "\n" + collateral_adjective[1:]
    return collateral_adjective_saved


def create_an_animal_array(table_data):
    new_animal_array = []
    animal_data_saved = ""
    for record in table_data.findAll('tr'):
        animal_data = ""
        for data in record.findAll('td')[0:1]:
            animal_data = animal_data + "," + data.text
            for data2 in record.findAll('td')[5:6]:
                animal_data = animal_data + "," + data2.text
        animal_data_saved = animal_data_saved + "\n" + animal_data[1:]
    for animal in animal_data_saved.split('\n'):
        if animal == '':
            pass
        else:
            new_animal_array.append(animal)
    return new_animal_array


def output_results_to_an_html_file(list_of_collateral_adjective, animal_array):
    html = "<html>\n<head></head>\n<style>p { margin: 0 !important; }</style>\n<body>\n"
    title = "All of the collateral adjectives and all of the animals which belong to it"
    html += '\n<p>' + title + '</p>\n'

    for item in list_of_collateral_adjective:
        para = '<p>' + ''.join(item + ": ") + '</p>\n'
        html += para
        for animal in animal_array:
            if item == animal:
                pass
            elif item in animal.split(',')[1]:
                para2 = '<p>' + ''.join(" - " + animal) + '</p>\n'
                html += para2
    with open('list_of_collateral_adjective.html', 'w', encoding='utf-8') as f:
        f.write(html + "\n</body>\n</html>")


def output_results_to_console(list_of_collateral_adjective, animal_array):
    for item in list_of_collateral_adjective:
        print(item + ": ")
        for animal in animal_array:
            if item in animal.split(',')[1]:
                print("- " + animal)


# __main__
if __name__ == "__main__":
    soup = make_soup(WIKI_URL)
    # find and Scraping second table
    table = soup.find_all('table', class_="wikitable")[1]
    # Collecting data:
    collateral_adjective_list = create_a_collateral_adjective_list(table)
    # sort the list of collateral adjective, delete duplicate and delete unnecessary characters
    collateral_adjective_list = list(dict.fromkeys(sorted(collateral_adjective_list.split())))[6:-1]
    # sort the list of animal & collateral adjective together
    animals_array = create_an_animal_array(table)

    # work with Thread
    start1 = time.perf_counter()
    with ThreadPoolExecutor(8) as executor:
        results = executor.map(output_results_to_an_html_file(collateral_adjective_list, animals_array))
    finish1 = time.perf_counter()
    print(f"Finished with threading in {round(finish1 - start1, 2)} seconds")
    # work without Thread
    start2 = time.perf_counter()
    output_results_to_console(collateral_adjective_list, animals_array)
    finish2 = time.perf_counter()
    print(f"Finished without threading in {round(finish2 - start2, 2)} seconds")
