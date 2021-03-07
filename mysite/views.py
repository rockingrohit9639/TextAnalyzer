from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
import string
import re
import requests
import json
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
import textwrap
from PyDictionary import PyDictionary
from textblob import TextBlob 

nltk.download('stopwords')
nltk.download('punkt')

#Api key for the meriam-webster api
api_key = "e7aa870d-ee6d-482c-a437-eb6bb0bcb9c1"

def index(request):

    return render(request, 'home.html')

def about(request):

    api_url='https://api.github.com/repos/rockingrohit9639/TextAnalyzer/contributors'

    response = requests.get(api_url).json()

    context = {
        "userData": response
    }

    return render(request, 'about.html', context)

def home(request):

    return render(request, 'index.html')


def index2(request):

    return render(request, 'index2.html')


def gallery(request):
    ACCESS_KEY = 'YBBd6J15p1YwXIV3THzl4Zt3eHiD3BGT8unud0VUNQo'
    place = request.session['user-input']
    payload = {
        'query': place,
        'client_id': ACCESS_KEY,
        'per_page': 40,
    }
    url = 'https://api.unsplash.com/search/photos'
    r = requests.get(url, params=payload).json()

    package = json.dumps(r, indent=2)
    arr = []
    for data in r['results']:
        arr.append(data['urls']['regular'])

    place=place.upper()+":"
    context = {
        'link': arr,
        'text': place,
    }
    return render(request, 'gallery.html', context)



def analyze(request):

    puncts = string.punctuation
    word_to_find = request.POST.get("word_input")
    djText = request.POST.get('text', 'default')
    remPunc = request.POST.get('removepunc', 'off')
    cap = request.POST.get('capitalize', 'off')
    small = request.POST.get('toSmall', 'off')
    upper = request.POST.get('toUpper', 'off')
    word_find_flag = request.POST.get('word_find', 'off')
    New_Line = request.POST.get('New_line', 'off')
    Emails= request.POST.get('Email_Address', 'off')
    Links = request.POST.get('Links', 'off')
    Passgen=request.POST.get('Password_Generator','off')
    search_word=request.POST.get('Search_word','off')
    gallery=request.POST.get('q','off')
    Suggest_word=request.POST.get('suggest_word','off')
    Sen_Analysis=request.POST.get('Sentiment', 'off')

    analyzed_text = ""
    word_status = ""

    

    countword = len(djText.split())

    if word_find_flag == "on":
        if word_to_find != "":
            if djText.find(word_to_find) != -1:
                word_status = "found"
                word=djText.replace(word_to_find,f"""<b style="color:{"red"};">"""+word_to_find+"</b>")
                djText=word

            else:
                word_status = "not found"
            
            analyzed_text = djText
            word_find="Find Word = " + word_to_find


            result = {
                "analyzed_text": analyzed_text,
                "highlight":"Chosen word is highlighted in red colour",
                "purpose": word_find,
                "status": word_status,
                "wordcount": countword,
                "analyze_text":True,
                "findWord":True
            }

    elif New_Line == "on":
        for char in djText:
            if char == '.':
                char='\n';
            analyzed_text = analyzed_text + char
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Changes '.' to New Line",
            "analyze_text":True,
            "wordcount": countword
        }
    elif Emails == "on":
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        lst= re.findall('\S+@+\S+', djText)
        tmp=""
        for x in lst:
            if(re.search(regex,x)):
                tmp+=x
                tmp+='\n'
        result = {
            "analyzed_text": tmp,
            "purpose": "Find All Emails",
            "analyze_text":True,
            "wordcount": countword
        }

    elif Passgen=="on":
        stop_words = set(stopwords.words('english'))
        chars = "!£$%&*#@"
        ucase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        text = re.sub(r'[^\w\s]', '', djText) 
        token = word_tokenize(text)

        filtered_sentence = []
        
        for w in token: 
            if w not in stop_words: 
                filtered_sentence.append(w)

        if len(filtered_sentence) > 0:
            random_word = random.choice(filtered_sentence)
        else:
            random_word = token[0]

        random_word=random_word.title()
    
        merge=""
        for word in random_word.split():
            merge+=random.choice(chars)+word[:-1]+ word[-1].upper()\
            +random.choice(string.ascii_letters)+"@"+random.choice(ucase_letters)\
            +random.choice(string.digits)+" "
        final_text=merge[:-1]
        result = {
            "analyzed_text": final_text,
            "purpose": "Generate password from text",
            "generate_text":True,
            "wordcount": countword
        }
        
    elif search_word=="on":
        url = 'https://www.dictionary.com/browse/'
        headers = requests.utils.default_headers() 
        headers.update({
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        })
        req = requests.get(url+djText, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        mydivs = soup.findAll("div", {"value": "1"})[0]
        for tags in mydivs:
            meaning = tags.text
        wrap = textwrap.TextWrapper(width=100) 
        word_meaning = wrap.fill(text=meaning) 
        result = {
            "analyzed_text": word_meaning,
            "purpose": "Searched Word",
            "generate_text":True,
            "wordcount": countword
        }

    
    elif Suggest_word=="on":
        find = requests.get(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{djText}?key={api_key}")
        response = find.json()
        
        if len(response) == 0:
            print("Word Not Recognized!")
        else:
            k=[]
            if str(response[0]).count(" ") == 0:
                for j in range(len(response)):
                    k.append(response[j])
                predict=" , ".join(k)
                djText=predict

            else:
                dictionary=PyDictionary()
                testdict=dictionary.synonym(djText)
                suggest=" , ".join(testdict)
                djText=suggest
            wrap = textwrap.TextWrapper(width=100) 
            suggest = wrap.fill(text=djText) 

        result = {
            "analyzed_text": suggest,
            "purpose": "Suggested Word",
            "generate_text":True,
            "wordcount": countword
        }
        
    elif Sen_Analysis=="on":
          
        djText=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", djText).split()) 

        analysis = TextBlob(djText) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            final=str(djText)+" (Positive Text)"
        elif analysis.sentiment.polarity == 0:
            final=str(djText)+" (Neutral Text)"
        else:
            final=str(djText)+" (Negative Text)"

        result = {
            "analyzed_text": final,
            "purpose": "Sentiment Analysis",
            "analyze_text":True,
            "wordcount": countword
        }
            

    elif gallery=="on":
        request.session['user-input']=djText
        result = {
            "analyzed_text": djText,
            "purpose":"Images",
            "status": "Press Button To View Images",
            "find_image": True,
            "generate_text":True,
            "wordcount": countword
        }                

        
    elif remPunc == "on" and cap == "on":

        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char

        analyzed_text = analyzed_text.capitalize()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations & Capitalize",
            "analyze_text":True,
            "wordcount": countword
        }
    elif remPunc == "on" and small == "on":
        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char

        analyzed_text = analyzed_text.lower()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations & To Small",
            "analyze_text":True,
            "wordcount": countword
        }

    elif remPunc == "on" and upper == "on":
        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char

        analyzed_text = analyzed_text.upper()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations & To Upper",
            "analyze_text":True,
            "wordcount": countword
        }

    elif cap == "on" and small == "on":
        analyzed_text = djText
        analyzed_text = analyzed_text.capitalize()
        analyzed_text = analyzed_text.lower()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize & To Small",
            "analyze_text":True,
            "wordcount": countword
        }

    elif cap == "on" and upper == "on":
        analyzed_text = djText
        analyzed_text = analyzed_text.capitalize()
        analyzed_text = analyzed_text.upper()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize & To Upper",
            "analyze_text":True,
            "wordcount": countword
        }
    elif small == "on" and upper == "on":
        analyzed_text = "Text can be smaller or uppercase only."
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Small & Upper",
            "analyze_text":True,
            "wordcount": countword
        }

    elif remPunc == 'on':
        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations",
            "analyze_text":True,
            "wordcount": countword
        }
    elif cap == "on":
        analyzed_text = djText.capitalize()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize",
            "analyze_text":True,
            "wordcount": countword
        }

    elif small == "on":
        analyzed_text = djText.lower()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "To Smallercase",
            "analyze_text":True,
            "wordcount": countword
        }

    elif upper == "on":
        analyzed_text = djText.upper()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "To Uppercase",
            "analyze_text":True,
            "wordcount": countword
        }
    elif Links == "on":
        pattern = '(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])'
        links = re.findall(pattern, djText, re.IGNORECASE)
        analyzed_text=""

        i = 0
        for x in links:
            i = i + 1
            analyzed_text+=f'<a href="{x}" target="_blank">Link {i}</a>'
            analyzed_text+='\n '

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Find All Links",
            "analyze_text":True,
            "wordcount": countword
        }    

    else:
        return HttpResponse('''<script type="text/javascript">alert("Please select atleast one option.");</script>''')

    return render(request, 'analyze.html', result)
