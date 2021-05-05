from bs4 import BeautifulSoup
from os.path import splitext
import os
import requests
import csv
from detect_color_image import detect_color_image

def get_soup(url, format=""):
    url = requests.get(url.format(format))
    url.encoding = "utf-8"
    soup = BeautifulSoup(url.text, "html.parser")
    return soup

def get_url_list(start_page=0, stop_page=10848):
    url_list = []
    for i in range(start_page, stop_page+1, 32):
        soup = get_soup('https://artistsnclients.com/browse?sort=price&dir=1&min=&max=&q=anime&offset={}', i)
        for tag in soup.select('.gradient_background > a'):
            url_list.append('https://artistsnclients.com' + tag['href'])
    return url_list

def get_like_list(start_page=0, stop_page=10848):
    rating_list = []
    for i in range(start_page, stop_page+1, 32):
        soup = get_soup('https://artistsnclients.com/browse?sort=price&dir=1&min=&max=&q=anime&offset={}', i)
        for tag in soup.select('.icon-thumbs-up.icon-white'):
            rating_list.append(tag.find_parent('span').text.strip())
    return rating_list

def get_price(url):
    soup = get_soup(url)
    return soup.select('.price_date_sec > button')[0].text.strip().lstrip('Base Price : $ ')

def get_duration(url):
    soup = get_soup(url)
    return soup.select('.price_date_sec > button')[1].text.strip().lstrip('Estimated Duration :').rstrip(' Day/s')
    
def get_img_url(url):
    soup = get_soup(url)
    return soup.select_one('img[itemprop="image"]')['src']

def get_bg(url):
    img_url = get_img_url(url)
    img_type = splitext(img_url)[1].lstrip('.')
    return 0 if img_type=='png' else 1

def get_artist_rating(url):
    soup = get_soup(url)
    next_url = 'https://artistsnclients.com' + soup.select_one('div.immi_slotartistname > a')['href']
    soup = get_soup(next_url)
    sum_rate = 0
    for rate in soup.select('span.stars'):
        sum_rate += int(rate['data-num-stars'])
    return sum_rate / len(soup.select('span.stars')) if len(soup.select('span.stars'))!=0 else 0.0

def get_completed(url):
    soup = get_soup(url)
    next_url = 'https://artistsnclients.com' + soup.select_one('div.immi_slotartistname > a')['href']
    soup = get_soup(next_url)
    return soup.select_one('.user_commiss > a > span').text.strip().rstrip(' Completed commissions')

def get_title(url):
    soup = get_soup(url)
    return soup.select_one('title').text.lower().strip()

def get_description(url):
    soup = get_soup(url)
    string = ''
    for str in soup.select('span.orange_text > p'): 
        string += str.text.lower().strip() + '\n'
    return string

def get_size(url):
    lst = []
    string = get_title(url) + get_description(url)
    if string.find('chibi')!=-1: lst.append("chibi")
    if string.find('half')!=-1: lst.append("half body")
    if string.find('full')!=-1: lst.append("full body")
    if string.find('bust')!=-1 or string.find('head')!=-1: lst.append("bust up")
    return ', '.join(lst) if lst else None

def save_image(url, i):
    lnk = get_img_url(url)
    os.makedirs('anime', exist_ok=True)
    os.chdir('anime')
    with open(f'img-{i}'+ splitext(lnk)[1], 'wb') as file:
        file.write(requests.get(lnk).content)
    os.chdir('..')
    return 'anime/' + file.name
