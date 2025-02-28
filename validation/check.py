import os, glob
import pytesseract
from PIL import Image
from strsimpy.weighted_levenshtein import WeightedLevenshtein


def teseract_recognition(path_img):
  return pytesseract.image_to_string(Image.open(path_img), lang='orus', config=r'--oem 3 --psm 6')

def insertion_cost(char):
  if char == '-':
    return 0
  return 1.0


def deletion_cost(char):
  if char == '-':
      return 0
  return 1.0


def substitution_cost(char_a, char_b):
  return 1.0


def main():
  total = 0
  count = 0
  max_len = 0
  weighted_levenshtein = WeightedLevenshtein(
    substitution_cost_fn=substitution_cost,
    insertion_cost_fn=insertion_cost,
    deletion_cost_fn=deletion_cost)
  for filename in glob.glob('images/*.tif'): #assuming gif
    im=Image.open(filename)
    txt = open('txt/' + os.path.split(filename.replace('image', 'text'))[1].split(".")[0]+'.txt')
    data = txt.read()
    if len(data) > max_len:
      max_len = len(data)

    metrics = weighted_levenshtein.distance(teseract_recognition(filename), data)
    print(f'[+] Расстояние между текстами: "{txt}" "{metrics/max_len}"')

    count = count + 1
    total = total + metrics

  print(f'[+] СРЕДНЕЕ: "{total/count/max_len}"')

if __name__ == "__main__":

  main()
