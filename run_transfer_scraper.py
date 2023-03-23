import transfer_scraper

player_transfer_scraper = transfer_scraper.TransferScraper()

final_players = player_transfer_scraper.scrape_players()

nationality_list, club_list = player_transfer_scraper.scrape_badges()

df = player_transfer_scraper.create_dataframe(final_players, nationality_list, club_list)
