from bs4 import BeautifulSoup
import requests
import pandas as pd

class TransferScraper:

    """
    This class is used to scrape player data from Transfermarkt.co.uk and create a pandas DataFrame with the results.

    Attributes:
    USER_AGENT (str): The user agent string to be used in HTTP requests.
    URL_TEMPLATE (str): The URL template for the Transfermarkt.co.uk website.
    headers (dict): The headers to be used in HTTP requests.

    Methods:
    scrape_webpage(): Scrapes a webpage given its URL and returns its HTML content as a BeautifulSoup object.
    scrape_players(): Scrapes the data of Premier League players from multiple pages and returns them as a list.
    scrape_badges(): Scrapes the club badge and nationality of Premier League players from multiple pages and returns them as a list.
    create_dataframe(): Creates a dataframe containing the scraped data.
    """
        
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    URL_TEMPLATE = 'https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1/page/{}'

    def __init__(self):

        """
        This method initializes the TransferScraper class by setting the headers to be used in HTTP requests.
        """

        self.headers = {'User-Agent': self.USER_AGENT}

    def scrape_webpage(self, url):

        """
        Scrapes a webpage given its URL and returns its HTML content as a BeautifulSoup object.

        Args:
        url (str): The URL of the webpage to be scraped.

        Returns:
        bs4.BeautifulSoup: A BeautifulSoup object containing the HTML content of the scraped webpage.
        """
                
        response = requests.get(url=url, headers=self.headers)
        return BeautifulSoup(response.content, 'html.parser')

    def scrape_players(self):

        """
        Scrapes the market values, name, position and age of Premier League players from multiple pages and returns them as a list.

        Returns:
        list: A list of Premier League player names, ages, position and market values.
        """

        all_players = []
        for pagenum in range(1, 5):
            url = self.URL_TEMPLATE.format(pagenum)
            soup = self.scrape_webpage(url)
            table = soup.find("table", class_='items')
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                all_players.append(cols)
        final_players = [all_players[i] for i in range(len(all_players)) if i % 3 == 0]
        return final_players

    def scrape_badges(self):

        """
        Scrapes the club badge and nationality of Premier League players from multiple pages and returns them as a list.

        Returns:
        list: 2 lists 1 of Premier League player clubs and 1 of their nationalities.
        """

        badge_list = []
        for pagenum in range(1, 5):
            url = self.URL_TEMPLATE.format(pagenum)
            soup = self.scrape_webpage(url)
            table = soup.find("table", class_='items')
            tbody = table.find("tbody")
            badges = tbody.find_all("td", class_="zentriert")
            for badge in badges:
                flags = badge.find_all('img')  
                if flags:  
                    first_flag = flags[0]  
                    first_badge = first_flag['title']
                    badge_list.append(first_badge)

        nationality_list = badge_list[::2]
        club_list = badge_list[1::2]

        return nationality_list, club_list

    def create_dataframe(self, players, nationalities, clubs):

        """
        Creates a dataframe from the lists from the previous methods

        Args:
        players (list): The list of players names, positions, age and rank
        nationalitis (list): A list of the players nationalities
        clubs (list): A list of the players clubs

        Returns:
        A dataframe containing all the information from the scraper
        """
        df = pd.DataFrame(players, columns=['Rank', 'null', 'null1', 'Player', 'Position', 'null3', 'Age', 'null4', 'Value'])
        df['Nationality'] = nationalities
        df['Club'] = clubs
        return df
