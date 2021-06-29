# https://stackoverflow.com/a/23035464

from PIL import Image, ImageStat
import requests

def detect_color_image(file, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    pil_img = Image.open(requests.get(file, stream=True).raw) if file.startswith('http') else Image.open(file)
    bands = pil_img.getbands()
    if bands == ('R','G','B') or bands== ('R','G','B','A'):
        thumb = pil_img.resize((thumb_size,thumb_size))
        SSE, bias = 0, [0,0,0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias)/3 for b in bias ]
        for pixel in thumb.getdata():
            mu = sum(pixel)/3
            SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
        MSE = float(SSE)/(thumb_size*thumb_size)
        if MSE <= MSE_cutoff:
            # print("grayscale\t")
            return 'grayscale'
        else:
            # print("Color\t\t\t")
            return 'color'
        # print("( MSE=",MSE,")")
    elif len(bands)==1:
        #print("Black and white", bands)
        return 'black and white'
    else:
        #print("Don't know...", bands)
        return 'don\'t know...'
