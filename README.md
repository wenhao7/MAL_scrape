# MAL_scrape
Python scripts to scrape information from popular anime database/community [MyAnimeList](https://myanimelist.net).

***

## Contents
<ul>
  <li> <code>scrape_anime_info.py</code> - Script contains the functions used to scrape content information related to all anime titles on the site that have a community-rated score. The first page of reviews for each title is also scraped.</li>
  <li> <code>scrape_anime_user_info.py</code> - Script contains the functions to periodically scrape a list of recently active users on the site, and to scrape each username's personal anime list where they keep track of titles that have watched and rated.</li>
  <li> <code>anime_info.csv</code> - .csv file containing the 13300 titles identified and scraped.</li>
  <li> <code>anime_reviews_sample.csv</code> - .csv file containing a sample of the review data scraped using the scripts due to size constraints</li>
  <li> <code>user_ratings_sample.csv</code> - .csv file containing a sample of the user ratings data scraped using the scripts due to size constraints</li>
</ul>


Columns within <code>anime_info.csv</code>:</code>
 <li><code>MAL_Id:</code>  Unique identifier id on the website</li>
 <li><code>Name:</code>  Main title used on the website</li>
 <li><code>Synonyms/Japanese/English_Name:</code>  Alternative titles</li>

 <li><code>Type:</code>  Release format of the title (i.e. direct-to-video, aired on tv, etc)</li>
 <li><code>Episodes:</code>  Number of episodes</li>
 <li><code>Status:</code>  Current airing status</li>
 <li><code>Aired:</code>  Run period</li>
 <li><code>Premiered:</code>  Premiere date</li>
 <li><code>Producers/Licensors/Studios:</code>  As named</li>

 <li><code>Source:</code>  Source material medium</li>
 <li><code>Genres:</code>  Genre of the title</li>
 <li><code>Demographic:</code>  Target audience</li>
 <li><code>Duration:</code>  Run length</li>

 <li><code>Rating:</code>  Content rating</li>
 <li><code>Score:</code>  Aggregated community score for the title</li>
 <li><code>Ranked:</code>  Ranking on the website based on "Score"</li>
 <li><code>Popularity:</code>  Popularity ranking of the title</li>
 <li><code>Members:</code>  Number of users who have the title within their list</li>
 <li><code>Favorites:</code>  Number of users who have favorited the title</li>

 <li><code>Watching/Completed/On-Hold/Dropped/Plan to Watch:</code>  Number of users who have the title within their list in each status</li>
 <li><code>Total:</code>  Number of users who have the title within their list</li>

 <li><code>Score-10-1:</code>  Number of users who have given the title each score from 10 to 1</li>
 <li><code>Synopsis:</code>  Description of the title</li>
 <li><code>Voice_Actors:</code>  Voice actors appearing on the main page of the title (Usually contains main characters and main supporting characters)</li>

 <li><code>Recommended_Ids:</code>  "MAL_Ids" of other titles that user have recommended for people who likes the current title.</li>
 <li><code>Recommended_Counts:</code>  Number of recommendation tied to the "Recommended_Ids"<li>
