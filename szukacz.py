import requests
from bs4 import BeautifulSoup
from googlesearch import search

def search_transport_companies(query, num_companies):
    companies = []
    for result in search(query, num_results=num_companies, lang='pl'):
        companies.append(result)
    return companies

def get_company_details(company_url):
    details = {}

    # Wysyłamy zapytanie HTTP do strony firmy
    response = requests.get(company_url)
    if response.status_code == 200:
        # Jeśli udało się pobrać stronę, przetwarzamy jej zawartość
        soup = BeautifulSoup(response.content, 'html.parser')

        # Przykładowe wypełnienie informacji o firmie na podstawie analizy strony
        # Dostosuj kod do struktury i układu strony firmy
        litres = soup.find('span', class_='litres')
        earnings = soup.find('div', class_='earnings')
        province = soup.find('div', class_='location')
        contact = soup.find('div', class_='contact')

        if litres:
            details['litres'] = litres.text
        if earnings:
            details['earnings'] = earnings.text
        if province:
            details['province'] = province.text
        if contact:
            details['contact'] = contact.text

    return details

# Główna część programu
query = 'firmy transportowe'
num_companies = int(input("Podaj ilość firm do wyszukania: "))

company_urls = search_transport_companies(query, num_companies)

for i, url in enumerate(company_urls, 1):
    print(f"--- Firma {i} ---")
    print("Adres URL:", url)
    details = get_company_details(url)
    if details:
        if 'litres' in details:
            print("Litrów w tankowaniu:", details['litres'])
        if 'earnings' in details:
            print("Zarobki:", details['earnings'])
        if 'province' in details:
            print("Województwo:", details['province'])
        if 'contact' in details:
            print("Kontakt:", details['contact'])
    else:
        print("Brak danych o firmie")

    print()

    # Zapisywanie danych do pliku
    with open('skan.txt', 'a') as file:
        file.write(f"--- Firma {i} ---\n")
        file.write("Adres URL: " + url + "\n")
        if 'litres' in details:
            file.write("Litrów w tankowaniu: " + details['litres'] + "\n")
        if 'earnings' in details:
            file.write("Zarobki: " + details['earnings'] + "\n")
        if 'province' in details:
            file.write("Województwo: " + details['province'] + "\n")
        if 'contact' in details:
            file.write("Kontakt: " + details['contact'] + "\n\n")
        else:
            file.write("Brak danych o firmie\n\n")
