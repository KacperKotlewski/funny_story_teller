from bs4 import BeautifulSoup
import requests
import string
from googletrans import Translator

japanise_fucking_numbers = {
    "１":"1",
    "２":"2",
    "３":"3",
    "４":"4",
    "５":"5",
    "６":"6",
    "７":"7",
    "８":"8",
    "９":"9",
    "０":"0",
    " ":"",
}
language = "en"


def translate(my_string):
    replaceDict = japanise_fucking_numbers    
    for key, replacement in replaceDict.items():  
        my_string = my_string.replace( key, replacement )

    return my_string

def inp(question=""):
    inp = input(question)
    try:
        return int(inp)%3000
    except:
        return sum([int(ord(i)) for i in inp])%3000

def iter_subpage(val, job_elems):
    for job in job_elems[::-1]:
        text = translate(job.text)
        last_val = None
        try:
            for i in range(2,7):
                last_val = (int(text[:i]))
        except:
            pass
        finally:
            if val == last_val:
                return text.replace(str(last_val), "").replace("0", "")

def scrap_sub_page(val, url):
    results = scrap_base(url).find(id="content_area")
    job_elems = results.find_all('p')
    last_section = None
    text = iter_subpage(val, job_elems)
    return text

def scrap_google_translate(val, src='ja', dest=language):
    try:
        translator = Translator()
        results = translator.translate(val, src=src, dest=dest)
        return (results.text)
    except Exception as e:
        print(e)
        input()
        quit()
    


def scrap_base(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def scrap_main_page(val):
    URL = 'https://batugameserifu.jimdofree.com/'
    results = scrap_base(URL).find("table")
    job_elems = results.find_all('td')

    last_section = None
    first_val = int(((job_elems[::-1])[0]).text[:-2])
    for job in job_elems[::-1]:
        section = job.find_all('a')[0]
        value = int(section.text[:-1])
        if val > first_val:
            return scrap_sub_page(val, URL+section['href'][1:])
        elif val < value:
            last_section = section
        else:
            return scrap_sub_page(val, URL+section['href'][1:])

def Try_play(i=""):
    text = (scrap_main_page(i))
    text = text.replace(str("□□"),str(name1))
    text = text.replace(str("○○"),str(name2))
    text = scrap_google_translate(text, dest=language)
    text = text.replace('"',"")
    text = text.replace('"',"")
    print(text)
    from gtts import gTTS 
    import os 
    myobj = gTTS(text=text, lang=language, slow=False) 
    myobj.save("read.mp3") 
    
    import playsound
    playsound.playsound('read.mp3', True)
    os.remove('read.mp3')

if __name__ == "__main__":
    language = input("enter your country shortcut (for example: en, es, pl): ")
    name1 = input(scrap_google_translate("type first name: ", src='en', dest=language))
    name2 = input(scrap_google_translate("type second name: ", src='en', dest=language))

    if input("automatated [y/n]: ") != "y":
        while True:
            inpt = inp(scrap_google_translate("whatever you type we will find something for you: ", src='en', dest=language))
            i=0
            while True:
                try:
                    Try_play(inpt+i)
                    break
                except:
                    i+=1
    else:
        that_was = []
        import random
        for i in range(3000):
            while True:
                r = random.randint(0, 3000)
                if not r in that_was:
                    try:
                        Try_play(r)
                        break
                    except:
                        pass
                    that_was.append(r)
                    break

