import pickle
import requests

if __name__ == "__main__":
    """
    Artist Page Pickles

    This creates pickle files from requests.get objects to be used as mock data for scraper testing
    """

    brand_new_band_artist_page = requests.get("https://en.wikipedia.org/wiki/Brand_New_(band)")
    with open("./tests/mock/brand_new_band.pickle", 'wb') as file:
        pickle.dump(brand_new_band_artist_page, file)

    death_cab_discog_page = requests.get("https://en.wikipedia.org/wiki/Death_Cab_for_Cutie_discography")
    with open("./tests/mock/death_cab_discog.pickle", 'wb') as file:
        pickle.dump(death_cab_discog_page, file)

    motion_city_artist_page = requests.get("https://en.wikipedia.org/wiki/Motion_City_Soundtrack")
    with open("./tests/mock/motion_city_artist.pickle", 'wb') as file:
        pickle.dump(death_cab_discog_page, file)

    """
    Album Page Pickles
    """

    brand_new_yfw_notag_page = requests.get("https://en.wikipedia.org/wiki/Your_Favorite_Weapon")
    with open("./tests/mock/brand_new_yfw_album_page.pickle", 'wb') as file:
        pickle.dump(brand_new_yfw_notag_page, file)
    
    death_cab_plans_album_page = requests.get("https://en.wikipedia.org/wiki/Plans_(album)")
    with open("./tests/mock/death_cab_plans_album_page.pickle", 'wb') as file:
        pickle.dump(death_cab_plans_album_page, file)
    
    motion_city_artalbum_page = requests.get("https://en.wikipedia.org/wiki/Go_(Motion_City_Soundtrack_album)")
    with open("./tests/mock/motion_city_artalbum_page.pickle", 'wb') as file:
        pickle.dump(motion_city_artalbum_page, file)

    """
    Track/Lyric Page Pickles
    """

