import transfer_scraper
import boto3
import unicodedata

player_transfer_scraper = transfer_scraper.TransferScraper()

final_players = player_transfer_scraper.scrape_players()

nationality_list, club_list = player_transfer_scraper.scrape_badges()

df = player_transfer_scraper.create_dataframe(final_players, nationality_list, club_list)

df = df.drop(['null', 'null1', 'null3', 'null4'], axis=1)
df['Age'] = df['Age'].astype(int)
df['Value'] = df['Value'].str.replace('€', '').str.replace('.00m', '000000')
df['Value'] = df['Value'].astype(int)
df['Player'] = df['Player'].str.replace('Ø', 'O')

def normalize_string(s):
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')

df['Player'] = df['Player'].apply(normalize_string)

df.to_csv('transfermarkt_data.csv', index=False)

s3_client = boto3.client('s3')
response = s3_client.upload_file('transfermarkt_data.csv', 'transfermarktdata', 'transfermarkt_data.csv' )
