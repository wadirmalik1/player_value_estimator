import transfer_scraper

player_transfer_scraper = transfer_scraper.TransferScraper()

# call the find_player_detail method
final_players = player_transfer_scraper.scrape_players()

# call the find_badges method
nationality_list, club_list = player_transfer_scraper.scrape_badges()

print(f'total players: {len(final_players)}')
print(f'total nationality: {len(nationality_list)}')
print(f'total clubs: {len(club_list)}')

# call the create_pd method
df = player_transfer_scraper.create_dataframe(final_players, nationality_list, club_list)
