from bs4 import BeautifulSoup
import requests
import pandas as pd

class TransfermarktScraper:

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    url_temp = "https://www.transfermarkt.co.uk/jumplist/startseite/wettbewerb/{}"
    league_codes = ["AN1L", "AR1N", "AUS1", "A1", "BGD1", "BE1", "BO1A", "BRA1", "CDN1", "CLPD", "CSL", "COLP", "COL1", "CRPD", "PDV1", 
                    "KR1", "TS1", "DK1", "EL1A", "EL1S", "SL1A", "GB1", "GB2", "GB3", "GB4", "FIJ1", "FR1", "FR2", "L1", "L2", "L3", "GHPL", 
                    "GR1", "GU1A", "GU1C", "HGKG", "UNG1", "IND1", "IN1L", "IRN1", "IR1", "ISR1", "IT1", "IT2", "JPL1", "JAP1", "RSK1", 
                    "KG1L", "MYS1", "MEXA", "MARP", "MO1L", "MYA1", "NPL1", "NL1", "NCL1", "NNL1", "NO1", "PN1A", "PN1C", "PR1A", "PR1C", 
                    "TDeA", "TDeC", "PFL1", "PL1", "PO1", "QSL", "RO1", "RU1", "SA1", "SC1", "SER1", "SIN1", "SFA1", "ES1", "ES2", "SE1", 
                    "C1", "TAD1", "THA1", "TUN1", "TUSC", "TR1", "UKR1", "UAE1", "MLS1", "URU1", "UZ1", "VZ1L", "VIE1"]
    
    list_seasons = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]

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
                list_urls.append("https://www.transfermarkt.co.uk" + team_links)

        return list_urls
    
    def scrape_player_links(self, list_urls):

        list_player_url = set()
        for link in list_urls:
            print(link)
            r = requests.get(url=link, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find("table", class_='items')

            if table is not None:
                tbody = table.find("tbody")
                rows = tbody.find_all("tr")
                for row in rows:
                    cells = row.find_all('td', 'hauptlink')
                    if cells:
                        player_link = cells[0].find('a')['href']
                        list_player_url.add("https://www.transfermarkt.co.uk" + player_link)
            else:
                print("Table with class 'items' not found on the page.")

        list_player_url = list(list_player_url)