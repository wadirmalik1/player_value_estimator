from bs4 import BeautifulSoup
import requests
import pandas as pd

class TransfermarktScraper:

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    url_temp = "https://www.transfermarkt.co.uk/jumplist/startseite/wettbewerb/{}"
    league_codes = ["GB1", "FR1", "L1", "IT1", "ES1"]
    list_seasons = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

    def __init__(self):
        self.headers = {'User-Agent': self.USER_AGENT}

    def scrape_webpage(self, url):

        response = requests.get(url=url, headers=self.headers)
        return BeautifulSoup(response.content, 'html.parser')
    
    def scrape_team_links(self):

        list_urls = []
        for codes in self.league_codes:
            url = self.url_temp.format(codes)
            soup = self.scrape_webpage(url)
            table = soup.find("table", class_='items')
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            for row in rows:
                team_links = row.select('a')[0]['href']
                print(team_links)
                list_urls.append(team_links)

        return list_urls
    
    def scrape_player_links(self, list_urls):

        list_player_url = set()
        for link in list_urls:
            url = link
            soup = self.scrape_webpage(url)
            table = soup.find("table", class_='items')
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td', 'hauptlink')
                if cells:
                    player_link = cells[0].find('a')['href']
                    list_player_url.add("https://www.transfermarkt.co.uk" + player_link)

        list_player_url = list(list_player_url)