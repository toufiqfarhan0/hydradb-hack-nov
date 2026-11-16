import os
import shutil
from PIL import Image, ImageChops

dest_dirs = [
    r'C:\Users\toufi\Downloads\lucen-blog-images',
    r'C:\Users\toufi\Desktop\lucen-blog-images'
]

def trim_whitespace(im):
    # If image has white margins around the dark card, crop exactly to the dark card
    bg = Image.new('RGB', im.size, (255, 255, 255))
    if im.mode != 'RGB':
        im_rgb = im.convert('RGB')
    else:
        im_rgb = im
    diff = ImageChops.difference(im_rgb, bg)
    bbox = diff.getbbox()
    if bbox:
        # Add a tiny 4px border so nothing touches the edge
        w, h = im.size
        pad = 2
        bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(w, bbox[2]+pad), min(h, bbox[3]+pad))
        return im.crop(bbox)
    return im

for d in dest_dirs:
    for fname in os.listdir(d):
        if fname.endswith('.png'):
            fpath = os.path.join(d, fname)
            try:
                with Image.open(fpath) as im:
                    orig_size = im.size
                    cropped = trim_whitespace(im)
                    new_size = cropped.size
                cropped.save(fpath, optimize=True)
                print(f"Trimmed {fname}: {orig_size} -> {new_size}")
            except Exception as e:
                print(f"Error on {fname}: {e}")

print("Successfully trimmed all blog PNGs!")
