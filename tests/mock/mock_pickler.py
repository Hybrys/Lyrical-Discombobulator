import pickle
import requests

if __name__ == "__main__":
    """
    Artist Page Pickles

    This creates pickle files from requests.get objects to be used as mock data for scraper testing
    """

    brand_new_band_artist_page = requests.get("https://en.wikipedia.org/wiki/Brand_New_(band)")
    with open("./tests/mock/brand_new_band.pickle", "wb") as file:
        pickle.dump(brand_new_band_artist_page, file)

    death_cab_discog_page = requests.get("https://en.wikipedia.org/wiki/Death_Cab_for_Cutie_discography")
    with open("./tests/mock/death_cab_discog.pickle", "wb") as file:
        pickle.dump(death_cab_discog_page, file)

    motion_city_artist_page = requests.get("https://en.wikipedia.org/wiki/Motion_City_Soundtrack")
    with open("./tests/mock/motion_city_artist.pickle", "wb") as file:
        pickle.dump(motion_city_artist_page, file)

    rem_titled_artist_page = requests.get("https://en.wikipedia.org/wiki/R.E.M._discography")
    with open("./tests/mock/rem_titled_artist_page.pickle", "wb") as file:
        pickle.dump(rem_titled_artist_page, file)

    """
    Album Page Pickles
    """

    brand_new_yfw_notag_page = requests.get("https://en.wikipedia.org/wiki/Your_Favorite_Weapon")
    with open("./tests/mock/brand_new_yfw_album_page.pickle", "wb") as file:
        pickle.dump(brand_new_yfw_notag_page, file)
    
    death_cab_plans_album_page = requests.get("https://en.wikipedia.org/wiki/Plans_(album)")
    with open("./tests/mock/death_cab_plans_album_page.pickle", "wb") as file:
        pickle.dump(death_cab_plans_album_page, file)
    
    motion_city_artalbum_page = requests.get("https://en.wikipedia.org/wiki/Go_(Motion_City_Soundtrack_album)")
    with open("./tests/mock/motion_city_go_artalbum_page.pickle", "wb") as file:
        pickle.dump(motion_city_artalbum_page, file)

    dylan_bob_dylan_typeerror_page = requests.get("https://en.wikipedia.org/wiki/Dylan_(Bob_Dylan_album)")
    with open("./tests/mock/dylan_bob_dylan_typeerror_page.pickle", "wb") as file:
        pickle.dump(dylan_bob_dylan_typeerror_page, file)


    """
    Track/Lyric Page Pickles
    """

    brand_new_yfw_songlyricsdotcom = requests.get("http://www.songlyrics.com/brand-new/failure-by-design-lyrics/")
    with open("./tests/mock/brand_new_yfw_songlyricsdotcom.pickle", "wb") as file:
        pickle.dump(brand_new_yfw_songlyricsdotcom, file)

    death_cab_plans_azlyrics = requests.get("https://www.azlyrics.com/lyrics/deathcabforcutie/brothersonahotelbed.html")
    with open("./tests/mock/death_cab_plans_azlyrics.pickle", "wb") as file:
        pickle.dump(death_cab_plans_azlyrics, file)
    

    """
    Lyric Comparisons From String Pickles
    """
    brand_new_lyrics = """Watch you on the one's and two's
Through a window in a well lit room
Become a recluse
And I blame myself 'cause I make things hard
And you're just trying to help

And when I wake up you're the first to call
This is one more late night basement song
And I'm so sore
My voice has gone to hell
This is one more sleepless night because we

Don't believe in filler, baby
If I could, I'd sit this out

(This is over when I say it's over)
This is a lesson in procrastination
I kill myself because I'm so frustrated
And every single second that I put it off
Means another lonely night, I gotta race the clock

(I ignore it and it ignores me too)
Let's say we go and crash your car?
And every time I leave you go and lock the door
And I walk myself pickin' at a chip on my shoulder
I'm another day late and one year older
It's failure by design

And we just want to sleep
But this night is hell
I'm sick and sunk and I blame myself
'Cause I make things hard
And you were tryin' to help

I got no gas windin' out my gears
  (No gas)
This is one more day on the verge of tears
And now my head hurts
  (Head hurts)
And my health is a joke and now I gotta stop
Because the headphones broke

We don't believe in filler, baby
If I could I'd sit this out

(This is over when I say it's over)
This is a lesson in procrastination
I kill myself because I'm so frustrated
And every single second that I put it off
Means another lonely night, I gotta race the clock

(I ignore it and it ignores me too)
Let's say we go and crash your car?
And every time I leave you go and lock the door
And I walk myself pickin' at a chip on my shoulder
I'm another day late and one year older
It's failure by design

I'm out of everything
No one sleeps till we get this shit
Out on the shelves
It's late, I'm faltering
This time, I got nothin' to say besides

Do do do, do do do
  ([Incomprehensible])
Do do do, do do do
Do do do, do do do
  ([Incomprehensible])
Do do do, do do do

Do do do, do do do
  ([Incomprehensible])
Do do do, do do do
Do do do, do do do
Nothing to say besides

(This is over when I say it's over)
This is a lesson in procrastination
I kill myself because I'm so frustrated
And every single second that I put it off
Means another lonely night, I gotta race the clock

(I ignore it and it ignores me too)
Let's say we go and crash your car?
And every time I leave you go and lock the door
And I walk myself pickin' at a chip on my shoulder
I'm another day late and one year older
I'm a failure by design"""

    with open("./tests/mock/brand_new_lyrics.pickle", "wb") as file:
        pickle.dump(brand_new_lyrics, file)
    
    death_cab_lyrics = """You may tire of me as our December sun is setting because I'm not who I used to be
No longer easy on the eyes but these wrinkles masterfully disguise
The youthful boy below who turned your way and saw 
Something he was not looking for: both a beginning and an end 
But now he lives inside someone he does not recognize 
When he catches his reflection on accident 

On the back of a motor bike 
With your arms outstretched trying to take flight 
Leaving everything behind 
But even at our swiftest speed we couldn't break from the concrete 
In the city where we still reside. 
And I have learned that even landlocked lovers yearn for the sea like navy men 
Cause now we say goodnight from our own separate sides 
Like brothers on a hotel bed 
Like brothers on a hotel bed 
Like brothers on a hotel bed 
Like brothers on a hotel bed 

You may tire of me
As our December sun is setting
Because I'm not who I used to be"""

    with open("./tests/mock/death_cab_lyrics.pickle", "wb") as file:
        pickle.dump(death_cab_lyrics, file)