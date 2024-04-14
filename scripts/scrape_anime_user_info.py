import os
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
import random
import csv


req_head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
           'X-MAL-CLIENT-ID':'e09c24c7eb88c3f399d9bd1355b4e015'}


def sleep(t=3):
    """
    Implements a randomized sleep time to circumvent scrape detection when using fixed delays

    Parameters
    ----------
    t : int
        minimum sleep time, sleep time follows a normal distribution with mean of 1.5*parameter.

    Returns
    -------
    None.

    """
    rand_t = random.random() * (t) + t
    time.sleep(rand_t)
    print(f"Sleeping for {rand_t}s")
    
    
def write_new_row(file_name, l):
    """
    Helper function to write list values to csv as a new row

    Parameters
    ----------
    file_name : str
        File path or file name of the .csv file to write to.
    l : List
        List of values to write.

    Returns
    -------
    None.

    """
    with open(file_name,'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|',lineterminator='\n')
        for v in l:
            writer.writerow([v])
        
        
def get_data(link, req_head):
    """
    Helper function to send GET request to given link

    Parameters
    ----------
    link : str
        Target url to send GET request.
    req_head : Dict
        Request head to send with our request.

    Returns
    -------
    data : requests.models.Response
        response from our request.

    """
    for _ in range(3):
        try:
            sleep(0.5)
            data = requests.get(link, headers = req_head)
            if data.status_code == 403:
                print('-----------------------------403 error encountered, may have been rate limited or user list is restricted-----------------------------')
                #sleep(300)
                return None
            elif data.status_code != 200:
                print( f'-----------------------------{data.status_code} status code encountered-----------------------------')
                sleep(5)
                continue
            else:
                return data
        except:
            buffer_t = random.random() * (40) + 100
            sleep(buffer_t)
            continue
    print("-----------------------------Error getting request-----------------------------")
    print(time.asctime())
    
    
def extract_usernames(data, current_set):
    """
    Extract usernames from the username webpage

    Parameters
    ----------
    data : requests.models.Response
        response from our GET request for username webpage.
    current_set : Set
        Set containing unique usernames found thus far.

    Returns
    -------
    usernames : TYPE
        DESCRIPTION.

    """
    doc = BeautifulSoup(data.text)
    usernames = []
    for d in doc.find_all('td', class_='borderClass'):
        username = d.find('div').text
        if username not in current_set:
            usernames.append(username)
    return usernames

def get_anime_list(data, user_name, pos, ratings_list):
    """
    Extract json information into a list of dict

    Parameters
    ----------
    data : requests.models.Response
        response from our GET request for username webpage.
    user_name : str
        username string of our target user.
    pos : int
        id given to the username within this script.
    ratings_list : List
        List containing a dictionary of information for each username.

    Returns
    -------
    ratings_list : List
        List containing an updated dictionary of information for each username.
    """
    for i in range(len(data.json()['data'])):
        json = data.json()['data'][i]
        rating_entry = {
            "Username" : user_name,
            "User_Id" : pos,
            "Anime_Id" : json['node'].get('id', np.nan),
            "Anime_Title" : json['node'].get('title', np.nan),
            "Rating_Status" : json['list_status'].get('status', np.nan),
            "Rating_Score" : json['list_status'].get('score', np.nan),
            "Num_Epi_Watched" : json['list_status'].get('num_episodes_watched', np.nan),
            "Is_Rewatching" : json['list_status'].get('is_rewatching', np.nan),
            "Updated" : json['list_status'].get('updated_at', np.nan),
            "Start_Date" : json['list_status'].get('start_date', np.nan)
        }
        ratings_list.append(rating_entry)
    return ratings_list


def write_new_row_dict(file_name, d):
    """
    Helper function to write dict to csv as a new row

    Parameters
    ----------
    file_name : str
        File path or file name of the .csv file to write to.
    d : Dict
        Dictionary of keys and values to write to the file.

    Returns
    -------
    None.

    """
    if not file_name in os.listdir():
        with open(file_name,'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|',lineterminator='\n')
            headers = list(d[0].keys())
            writer.writerow(headers)
    with open(file_name,'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|',lineterminator='\n')
        for i in range(1,len(d)):
            values = []
            for k, v in d[i].items():
                values.append(str(v))
            writer.writerow(values)
            
#current_set = set()
def scrape_users(req_head, file_name='usernames_list.csv', target=20000):
    """
    Scrape usernames from the user page

    Parameters
    ----------
    req_head : Dict
        Request headers to include in our request.
    file_name : str, optional
        File path / file name of our .csv file to write to. The default is 'usernames_list.csv'.
    target : int, optional
        Our target number of usernames. The default is 20000.

    Returns
    -------
    None.

    """
    current_set = set(pd.read_csv(file_name, delimiter='|', header=None).values.ravel())
    i = 0
    #req_head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}
    while i < target:
        data = get_data('https://myanimelist.net/users.php', req_head)
        usernames = extract_usernames(data, current_set)
        current_set.update(usernames)
        
        write_new_row(file_name, usernames)
        i = len(current_set)
        print(f'Current number of usernames found: {i}')
        

def scrape_user_animelist(usernames, req_head, pos=0, log_file='skipped_users_list.csv', output_file='user_list_ratings.csv'):
    """
    Scrape anime list information of each username within the list of usernames

    Parameters
    ----------
    usernames : List
        List of usernames to scrape from.
    req_head : Dict
        Request headers to include in our request.
    pos : int, optional
        Current positional index from usernames. The default is 0.
    log_file : str, optional
        File path / file name of our .csv file to record usernames that encountered an error. The default is 'skipped_users_list.csv'.
    output_file : str, optional
        File path / file name of our .csv file to record our scraped data. The default is 'user_list_ratings.csv'.

    Returns
    -------
    None.

    """
    curr = 0 # track consecutive skipped users, to differentiate rate limiting vs user's restricted list
    while pos < len(usernames):
        # if 403 error encountered more than 3 times in a row, sleep for ~5 minutes due to suspected rate limiting
        if curr > 3:
            print("Suspected rate limiting, pausing for a few minutes")
            sleep(240)
        username = usernames[pos]
        animelist_link = f'https://api.myanimelist.net/v2/users/{username}/animelist?limit=500&nsfw=true&fields=list_status'
        ratings_list= []
        data = get_data(animelist_link, req_head)
        
        # log the users that were skipped due to 403 error, this can happen if website rate limits us or if the user has chosen to keep their list private/restricted.
        if data is None:
            print(f'Current number of usernames processed: {pos} / {len(usernames)}')
            print(f'Skipping user {pos} as rate limited or user list is restricted')
            write_new_row_dict('skipped_users_list.csv', [{'pos':pos, "username":username}])
            curr += 1
            pos += 1
            continue
        curr = 0
        ratings_list = get_anime_list(data, usernames[pos], pos, ratings_list)
        if len(ratings_list):
            write_new_row_dict('user_ratings.csv', ratings_list)
        
        print(f'Current number of usernames processed: {pos} / {len(usernames)}')
        pos += 1
    