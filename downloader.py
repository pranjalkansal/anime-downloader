import requests;
import os;
import logging;
import lxml;
import sys;

from bs4 import BeautifulSoup;

HELP = '''
Usage: downloader.py (search | -s) <keyword>
       downloader.py (download | -l) <link>
       downloader.py (help | -h)
       downloader.py (interactive)
Options:
    -h --help          Show this help message and exit
    -s, --search       Search with keyword
    -l, --link         Download anime using link.
Arguments:
    keyword           Anime keyword/name to search
    link              Link to anime page on nowtvshow.com
''';

# Global Variables.
ANIME_LINK = 'http://anime.nowtvshow.com/';
TOTAL_EPISODES = 0;

# Check command line arguments.
def check_argument_valid(args):

    # Check if user is asking for help only.
    if(args[0] in ['-h', '--help']):
        print(HELP);
        return False;
        
    # Check if user is passing keywords in arguments.
    if(args[0] in ['-s', '--search'] and len(args) > 1):
        args = args[1:];
        keyword = ' '.join(args);   # Create keyword string.
        keyword = keyword.strip();
        
        return ['search', keyword];
        
    # Check if correct link is inseted.
    if(args[0] in ['-l', '--link'] and len(args) == 2):
        if(args[1][0:len(ANIME_LINK)] == ANIME_LINK):  # Check if user enter correct site url.
            return ['link', args[1]];
        else:
            print('Incorrect link provided!!!');
    
    return False;        
    
# Fetch episode range from user.
def fetch_episode_range(total_episodes, qualities):
    try:
        start_episode = int(input('\nEnter starting episode: '));
        end_episode = int(input('\nEnter ending episode: '));
        quality = raw_input('\nEnter quality in ' + str(qualities) + ' : ');
    except:
        print('\n\nEnter valid episode number.')
        fetch_episode_range(total_episodes);
        
    check_condition = start_episode < 0 or start_episode > end_episode + 1;
    check_condition = check_condition or start_episode > total_episodes + 1;
    check_condition = check_condition or end_episode > total_episodes;
    check_condition = check_condition or end_episode < start_episode;
    check_condition = check_condition or not quality in qualities;
     
    if(check_condition):
        print('\n\n********************* Incorrect data entered ********************\n');
        print('\n\n---------------- Re-enter data ---------------------\n');
        fetch_episode_range(total_episodes, qualities);
        
    return {'start_episode': start_episode, 'end_episode': end_episode, 'quality': quality};

# Start downloading episodes.
def start_download(link, anime_name, anime_image, episode_name, synopsis, anime, total_episodes):
    if(not os.path.exists(anime_name)):
        os.mkdir(anime_name);
        
    file_path = os.getcwd() + '/' + anime_name + '/';
    
    # Write synopsis in a file.
    if(not os.path.exists(file_path + 'over_view')):
        open_file = open(file_path + 'over_view', 'w');
        open_file.write(synopsis.encode('utf-8'));
        open_file.close();
    
    # Save image file.
    if(not os.path.exists(file_path + anime_name +'.jpg')):
        open_file = open(file_path + anime_name +'.jpg', 'wb');
        for chunk in requests.get(anime_image):
            open_file.write(chunk);
        open_file.close();
    
    # Save video files.
    
    # Create link of user choice quality.
    link = link.split('/');
    
    split_point = '.';
    
    link_to_adjust = link[-1].split(split_point);
    file_format = link_to_adjust[-1];
    link_to_adjust[-4] = '%5B' + str(anime['quality']) + '%5D';
    
    if(episode_name.find('.') == -1):
        split_point = ' ';
    episode_name = episode_name.split(split_point);
    episode_name.pop();  # Remove Quality appended in episode name.
    episode_name.pop();  # Remove Episoe number.
    episode_name = split_point.join(episode_name);
    
    split_point = '.';
    
    for episode in range(int(anime['start_episode']), int(anime['end_episode']) + 1):
        prefix_zero = '0';
        for zero in range(len(str(episode)), len(str(total_episodes)) - 1):
            prefix_zero = prefix_zero + '0';
        link_to_adjust[-5] = prefix_zero + str(episode);
        
        link[-1] = split_point.join(link_to_adjust);
        link_to_fetch = '/'.join(link);
        
        _episode_name = episode_name + '.' +prefix_zero + str(episode);
        
        # Start saving video files.
        print('\nDownloading episode: ' + _episode_name);
        if(not os.path.exists(file_path + _episode_name + file_format)):
            open_file = open(file_path + _episode_name + '.' + file_format, 'wb');
            for chunk in requests.get(link_to_fetch).iter_content(chunk_size=1024):
                open_file.write(chunk);
            open_file.close();
        print('\n' + _episode_name + ' Downloaded successfully!!\n');    

# Fetch episode links.
def extract_link_info(link):
    # Fetch data from the anime link.
    html = BeautifulSoup(requests.get(link).text, 'lxml');
    
    # Extract image link.
    anime_name = link.split('/');
    anime_image = '';
    if(not anime_name[-1]):
        anime_name.pop();
        
    anime_name = anime_name.pop().title().replace('-', ' ');

    for image in html.find_all('img'):
        if(image.get('alt') and image.get('alt').lower().replace(':', '') == anime_name.lower()):
            anime_image = image.get('src');
    if(not anime_image):
        print('\n No image file found!!');
        
    # Extract data about anime.
    over_view = html.findChildren('div' , attrs = {'class': 'filmicerik'});
    
    anime_links = [];
    episode_name = [];
    anime_synopsis = '';
    
    for material in over_view:
        anime_synopsis = material.get_text();
        
        # Extract links to download.
        for link in material.find_all('a'):
            anime_links.append(link['href']);
            episode_name.append(link.get_text());
    
    anime_synopsis = anime_synopsis.split('\n\n');
    
    for text in anime_synopsis:
        if(len(text) > 5):
            anime_synopsis = text;
            break;
            
    # Extract anime quality, number of episodes and sort links in order.
    quality_aval = [];
    
    split_point = '.';
    if(episode_name[0] and episode_name[0].find(' ') > -1):
        split_point = ' ';
    
    iteration = 0;
    for episode in episode_name:
        split = episode.split(split_point);
        
        quality = split.pop();
        
        if(quality[0] == '[' and not quality[1:-1] in quality_aval):
            quality_aval.append(quality[1:-1]);
        else:
            if(not quality[0] == '[' and not quality[:-1] in quality_aval):
                quality_aval.append(quality[:-1]);
        
        iteration += 1;
    
    TOTAL_EPISODES = (iteration)/len(quality_aval);
    anime_links = anime_links[0];
    episode_name = episode_name[0];
    
    # Fetch episode range form user.
    user_input = raw_input('\nDownload all episodes? (y/n): ');
    
    if(user_input == 'n' or user_input == 'N'):
        episode = fetch_episode_range(TOTAL_EPISODES, quality_aval);
    
    else:
        episode = {'start_episode': 1, 'end_episode': TOTAL_EPISODES, 'quality': 720};
        
    start_download(anime_links, anime_name, anime_image, episode_name, anime_synopsis, episode, TOTAL_EPISODES);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
# Search for anime.
def search_anime(keyword):
    # Fetch search html.
    html = BeautifulSoup(requests.get(ANIME_LINK + '?s=' + keyword).text, 'html.parser');
    
    # Find search resuls.
    html = html.select('div .movief > a[href]');
    
    # Return if nothing found.
    if(not html):
        print('Sorry, no results found.');
        return False;
        
    # Store links and display anime name.
    store_links = [];
    search_anime_name = [];
    
    for anime in html:
        store_links.append(anime.get('href'));
        search_anime_name.append(anime.get_text());
        
    # User select the link.
    search_iter = 0;
    print('Search Complete: ' + str(len(search_anime_name)) + ' results found');
    for anime in search_anime_name:
        search_iter += 1;
        print('\n' + str(search_iter) + '. ' + anime);
    user_input = int(input('\n\nChoose appropriate link: '));
    
    link_to_use = store_links[user_input - 1];
    
    link_to_use = link_to_use.replace('\"', '');
    
    extract_link_info(link_to_use);
    
    
# Main startup function.

def main():
    if(sys.argv):
        args = sys.argv[1:]; # Command line arguments.
        args = check_argument_valid(args); # Get keyword or link by validating arguments.

        if(args):
            if(args[0] == 'search'):
                search_anime(args.pop());
            else:
                extract_link_info(args.pop());
    
    else:
        user_input = raw_input('\nEnter anime name to search: ');
        search_anime(user_input);
        
main();
