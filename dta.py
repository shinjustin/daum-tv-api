from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import requests
import sys

default_thumb = 'https://search1.daumcdn.net/search/statics/common/pi/noimg/img_size_fs_prof.png'

def merge_episode_rating_lists(episode_list, rating_list):
    pass

def parse_program(program_soup):
    program = dict()
    title = program_soup.find(class_='tit_program').strong.text.strip()
    ico_status = program_soup.find(class_='tit_program').find(class_='ico_status')
    if ico_status:
        is_airing = False
    else:
        is_airing = True
    poster = program_soup.find(class_='wrap_thumb').img['src']
    metadata = program_soup.find_all(class_='dl_comm dl_row')
    genre = None
    about = None
    crew_list_short = None
    websites = list()
    for md in metadata:
        field = md.dt.text.strip()
        value = md.dd.text.strip()
        if field == '장르':
            genre = value
            genre = genre.replace('\xa0', '')
        elif field == '소개':
            about = value
        elif field == '제작':
            # TODO: decide whether to add this in object
            # TODO: split crew list into individual objects
            crew_list_short = value
            crew_list_short = crew_list_short.replace('\xa0', '')
        elif field == '사이트':
            anchors = md.dd.find_all('a')
            for a in anchors:
                website = dict()
                name = a.text.strip()
                url = a['href']
                website['name'] = name
                website['url'] = url
                websites.append(website)
        elif field == '버튼모음':
            anchors = md.dd.find_all('a')
            for a in anchors:
                website = dict()
                name = a.text.strip()
                url = a['href']
                website['name'] = name
                website['url'] = url
                websites.append(website)

    program['title'] = title
    program['is_airing'] = is_airing
    program['poster'] = poster
    program['genre'] = genre
    program['about'] = about
    #program['crew_list_short'] = crew_list_short
    program['websites'] = websites

    return program

def parse_casting(casting_soup):
    cast_list_soup = casting_soup.find('div', class_='castingList').find_all('li')
    cast_list = list()
    for cast_soup in cast_list_soup:
        cast = dict()
        try:
            img = cast_soup.find('img')['src']
        except TypeError:
            img = default_thumb
        name = cast_soup.find('span', class_='txt_name').text.strip()
        role = cast_soup.find('span', class_='sub_name').text.strip()

        cast['img'] = img
        cast['name'] = name
        cast['role'] = role

        # TODO: create separate objects for actor and character for fiction show; currently gets character only
        '''
        actor = dict()
        actor[''] = None
        cast['actor'] = actor
        '''

        cast_list.append(cast)

    crew_list_soup = casting_soup.find('div', class_='lst').find_all('li')
    crew_list = list()
    for crew_soup in crew_list_soup:
        crew = dict()
        try:
            img = crew_soup.find('img')['src']
        except TypeError:
            img = default_thumb
        name = crew_soup.find('span', class_='txt_name').text.strip()
        role = crew_soup.find('span', class_='sub_name').text.strip()

        crew['img'] = img
        crew['name'] = name
        crew['role'] = role

        crew_list.append(crew)

    return cast_list, crew_list

def parse_episode(episode_soup):
    #char_url = f'https://search.daum.net/qsearch?mk={mk}&uk={uk}&q={char_id}&w=iron&m=tv_character&key={char_id}&viewtype=json'

    if not episode_soup:
        return None, None
    episode_list = list()
    episode_list_soup = episode_soup.find(id='clipDateList').find_all('li')
    for episode_soup in episode_list_soup:
        episode = dict()
        date = episode_soup['data-clip']
        date = datetime.strptime(date, '%Y%M%d')
        episode_id = episode_soup['data-episode']
        episode_text_name = episode_soup.find(class_='txt_episode').text.strip()
        episode_text_date = episode_soup.find(class_='f_nb').text.strip()

        episode['date'] = date
        episode['id'] = episode_id
        episode['text_name'] = episode_text_name
        episode['text_date'] = episode_text_date

        episode_list.append(episode)

    return episode_list

def parse_rating(rating_soup):
    if not rating_soup:
        return None
    rating_list = list()
    rating_list_soup = rating_soup.find('tbody').find_all('tr')
    for rating_soup in rating_list_soup:
        rating = dict()
        date = rating_soup.find_all('td')[0].text.strip()
        text_name = rating_soup.find_all('td')[1].text.strip()
        rate = rating_soup.find_all('td')[2].text.strip()
        rank = rating_soup.find_all('td')[3].text.strip()

        rating['date'] = date
        rating['text_name'] = text_name
        rating['rate'] = rate
        rating['rank'] = rank

        rating_list.append(rating)

    return rating_list

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def search(query):
    show = dict()

    query = query.replace(' ', '%20')
    url = f'https://search.daum.net/search?w=tv&q={query}&irt=tv-program&DA=TVP'
    soup = get_soup(url)

    tabs = soup.find(id='tabCont')

    program_soup = tabs.find(id='tv_program')
    program = parse_program(program_soup)

    casting_soup = tabs.find(id='tv_casting')
    cast_list, crew_list = parse_casting(casting_soup)

    episode_soup = tabs.find(id='tv_episode')
    episode_list = parse_episode(episode_soup)

    #schedule = tabs.find(id='tv_schedule')

    rating_soup = tabs.find(id='tv_rating')
    rating_list = parse_rating(rating_soup)

    #music = tabs.find(id='tv_music')

    show['program'] = program
    show['cast_list'] = cast_list
    show['crew_list'] = crew_list
    show['episode_list'] = episode_list
    # TODO: merge rating_list into episode_list
    #episode_list = merge_episode_rating_list(episode_list, rating_list)
    #show['rating_list'] = rating_list

    return show

if __name__ == '__main__':
    #query = sys.argv[1]
    queries = [
            #'신발 벗고 돌싱포맨',
            '오 마이 비너스',
            #'환승연애 2',
            #'으라차차 내 인생',
            ]
    for query in queries:
        show = search(query)
        pprint(show)
