from web_scraping import *
from PIL import UnidentifiedImageError
from os.path import exists

start_page = 0
stop_page = 32 # 32=>ดึง2หน้า, 64=>3หน้า, 96=>4หน้า, 128=>5หน้า, ..., 32*n => n+1 หน้า (ถ้าเริ่มจากหน้าแรก)

"""
ดึง 2 หน้าสุดท้าย
start_page = 10848
stop_page = 10880
"""

url = get_url_list(start_page, stop_page)
like_list = get_like_list(start_page, stop_page)

with open('web_scraping.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    if not exists('web_scraping.csv'):
        writer.writerow(['img url', 'img path', 'duration (day)', 'price ($)', 'size', 'color', 'background', 'like', 'artist rate', 'completed'])
    for i, j in enumerate(url):
        try:
            img_url = get_img_url(j)
            img_path = save_image(j, start_page+i)
            duration = get_duration(j)
            price = get_price(j)
            size = get_size(j)
            color = 1 if detect_color_image(img_url)=='color' else 0
            background = get_bg(j) if color==1 else 0
            like = like_list[i]
            artist_rate = get_artist_rating(j)
            completed = get_completed(j)
            description = get_description(j)
        except (AttributeError, TypeError, UnidentifiedImageError):
            pass
        writer.writerow([img_url, img_path, duration, price, size, color, background, like, artist_rate, completed])
