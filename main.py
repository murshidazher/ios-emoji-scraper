import re
import os
import urllib.request
import ssl
import glob
from PIL import Image
# ssl.OPENSSL_VERSION

def convert_yaml():
  with open('ex.txt') as f1:
    with open('ios13.yaml', 'w') as f2:
      lines = f1.readlines()
      for i, line in enumerate(lines):

        yaml_line = line.replace('{', '\n')
        yaml_line = yaml_line.replace('}\n', '')
        yaml_line = yaml_line.replace(',', '')
        yaml_line = yaml_line.lstrip();

        if yaml_line:
          yaml_line = '- title: ' + yaml_line
          yaml_line = yaml_line.replace(': "https', '\n  link: https')
          yaml_line = yaml_line.replace('.png', '.png\n  shortcode: ":text:')
          f2.write(yaml_line)

def download_img():
  base = "ios_emoji"
  i = 0
  with open('ex.txt') as f:
    urls = f.read()
    links = re.findall('"((http)s?://.*?)"', urls)
    for url in links:
        i = i+1
        print('Downloading... ' + str(i))
        context = ssl._create_unverified_context()
        img_url = url[0]
        path_url = img_url.replace('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/60/apple/237/', '')
        path_url = os.path.join(base, path_url)
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(img_url, path_url)

def resize():
  root_dir = "ios_emoji"
  out_dir = "resized"
  resize_ratio = 0.6  # where 0.5 is half size, 2 is double size
  
  i = 0
  for filename in glob.iglob(root_dir + '**/*.png', recursive=True):
      i = i + 1
      decimal_round = 3 # number of decimal points
      
      re_filename = os.path.join(out_dir, filename)
      im = Image.open(filename)

      new_image_height = int(im.size[0] / (1/resize_ratio))
      new_image_length = int(im.size[1] / (1 / resize_ratio))  
      imResize = im.resize((new_image_height, new_image_length), Image.ANTIALIAS)

      with open(re_filename, 'w+') as f:
        # (re_filename, 'PNG', optimize=True, quality=85)
        imResize.save(re_filename, 'PNG', compress_level=9) # lossless compression algorithm
        print('Converted... ' + str(i) + ' dimesion: ' + str(imResize.size[0]) +  'px size: ' + 'from ' + str(round(os.path.getsize(filename)/1024, decimal_round)) + 'KB to ' + str(round(os.path.getsize(re_filename)/1024, decimal_round)) + 'KB')

convert_yaml()
# download_img()
# resize()