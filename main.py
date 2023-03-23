import transfer_scraper
import boto3
import unicodedata

# Intialise scraper
player_transfer_scraper = transfer_scraper.TransferScraper()

# call function to scrape player data
final_players = player_transfer_scraper.scrape_players()

# call function to scrape club and national badges of players 
nationality_list, club_list = player_transfer_scraper.scrape_badges()

# call function to create dataframe from scraped data
df = player_transfer_scraper.create_dataframe(final_players, nationality_list, club_list)

# clean the data in the dataframe
df = df.drop(['null', 'null1', 'null3', 'null4'], axis=1)
df['Age'] = df['Age'].astype(int)
df['Value'] = df['Value'].str.replace('€', '').str.replace('.00m', '000000')
df['Value'] = df['Value'].astype(int)
df['Player'] = df['Player'].str.replace('Ø', 'O')

# function to clean special characters in player names
def normalize_string(s):
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')

df['Player'] = df['Player'].apply(normalize_string)

# convert dataframe to csv
df.to_csv('transfermarkt_data.csv', index=False)

#upload data to s3 bucket
s3_client = boto3.client('s3')
response = s3_client.upload_file('transfermarkt_data.csv', 'transfermarktdata', 'transfermarkt_data.csv' )
