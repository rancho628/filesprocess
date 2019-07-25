from legalfiles.models import Txt
import os


def save_txt(path, files):
    for p,f in zip(os.listdir(path),files):
        Txt.objects.get_or_create(title=p)
        Txt.objects.update_or_create(title=p, defaults={"content":f})




if __name__ == '__main__':
    save_txt()
