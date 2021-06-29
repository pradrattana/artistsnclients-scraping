from web_scraping import *
from PIL import UnidentifiedImageError
from os.path import exists

start_page = 0
stop_page = 10880

url = get_url_list(start_page, stop_page)
like_list = get_like_list(start_page, stop_page)

with open('web_scraping.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    if not exists('web_scraping.csv'):
        writer.writerow(['url', 'path', 'price', 'day', 'like', 'completed', 'rate', 'size', 'color', 'bg'])
    for i, j in enumerate(url):
        try:
            url = get_img_url(j)
            path = save_image(j, start_page+i)
            price = get_price(j)
            day = get_duration(j)
            like = like_list[i]
            completed = get_completed(j)
            rate = get_artist_rating(j)
            size = get_size(j)
            color = 1 if detect_color_image(img_url)=='color' else 0
            bg = get_bg(j) if color==1 else 0
            description = get_description(j)
        except (AttributeError, TypeError, UnidentifiedImageError):
            pass
        writer.writerow([url, path, price, day, like, completed, rate, size, color, bg])
