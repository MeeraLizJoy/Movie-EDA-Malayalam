import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def scrape_malayalam_movies(year):
    url = f'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_{year}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    print(f"Scraping year: {year}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}, status code: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all('table', class_='wikitable')
    print(f"Found {len(tables)} 'wikitable' tables on page for year {year}")
    movie_titles = []
    
    for table in tables:
        rows = table.find_all('tr')[1:]  # skip header row
        for row in rows:
            cols = row.find_all('td')
            if cols:
                # Try first column, if empty try second column as some tables differ
                title = cols[0].get_text(strip=True)
                if not title and len(cols) > 1:
                    title = cols[1].get_text(strip=True)
                title = re.sub(r'\[.*?\]', '', title)
                if title:
                    movie_titles.append(title)
    
    print(f"Found {len(movie_titles)} movies for year {year}")
    return movie_titles

if __name__ == '__main__':
    start_year = 1998
    end_year = 2024
    all_titles = []
    
    for y in range(start_year, end_year + 1):
        titles = scrape_malayalam_movies(y)
        all_titles.extend(titles)
        time.sleep(3)  # polite delay
    
    unique_titles = list(set(all_titles))
    df = pd.DataFrame(unique_titles, columns=['title'])
    df.to_csv('data/malayalam_movie_titles.csv', index=False)
    print(f"Scraped a total of {len(unique_titles)} unique Malayalam movie titles.")
