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
import random


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

def get_synonyms(word):
    try:
        synonyms=[]
        res = requests.get('https://www.merriam-webster.com/dictionary/'+word)
        soup = BeautifulSoup(res.text, 'lxml')
        containers=soup.findAll(
            'ul',{'class':'mw-list'})[0].findAll('li')
        for con in containers:
            synonyms.append(con.find("a").text)
        return synonyms
    except:
        dictionary=PyDictionary()
        testdict=dictionary.synonym(word)
        return testdict

def get_example(word):
    try:
        res = requests.get('https://www.merriam-webster.com/dictionary/'+word)
        soup = BeautifulSoup(res.text, 'lxml')
        containers=soup.find("div",{'class':'in-sentences'}).text
        example=' '.join(containers.split()).split('.')[3].strip()
        return example
    except:
        return None

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
    remPunc = request.POST.get('option','removepunc')
    cap = request.POST.get('option','capitalize')
    small = request.POST.get('option','toSmall')
    upper = request.POST.get('option', 'toUpper')
    word_find_flag = request.POST.get('option','word_find')
    New_Line = request.POST.get('option','New_line')
    Emails= request.POST.get('option','Email_Address')
    Links = request.POST.get('option','Links')
    Passgen=request.POST.get('option', 'Password_Generator')
    search_word=request.POST.get('option', 'Search_word')
    gallery=request.POST.get('option', 'q')
    Suggest_word=request.POST.get('option', 'suggest_word')
    Sen_Analysis=request.POST.get('option', 'Sentiment')
    Synonyms=request.POST.get('option', 'Synonyms')

    analyzed_text = ""
    word_status = ""

    

    countword = len(djText.split())

    if word_find_flag == "word_find":
        if word_to_find != "":
            if djText.find(word_to_find) != -1:
                word_status = "found"
                word=djText.replace(word_to_find,f"""<b style="color:{"red"};">"""+word_to_find+"</b>")
                djText=word   
   
                try:
                    synonym_01=get_synonyms(word_to_find)
                    synonyms2=random.sample(synonym_01,4)

                    final=""
                    for f in synonyms2:
                        final+=f+" , "

                    example=get_example(word_to_find)

                    synonyms=final+example

                except:
                    synonyms="Not Available"

            else:
                word_status = "not found"
                synonyms="Text Not Found"
            
            analyzed_text = djText
            word_find="Find Word = " + word_to_find
            synonym=format_html('<b style="color:{};">{}</b>','green',synonyms)

            result = {
                "analyzed_text": analyzed_text,
                "highlight":"Chosen word is highlighted in red colour and synonyms/examples in green colour",
                "purpose": word_find,
                "status": word_status,
                "synonym":synonym,
                "wordcount": countword,
                "analyze_text":True,
                "findWord":True
            }


    elif New_Line == "New_line":
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
    elif Emails == "Email_Address":
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

    elif Passgen=="Password_Generator":
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
        
    elif search_word=="Search_word":
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

    
    elif Suggest_word=="suggest_word":
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
        
    elif Sen_Analysis=="Sentiment":
          
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
        
    elif gallery=="q":
        request.session['user-input']=djText
        result = {
            "analyzed_text": djText,
            "purpose":"Images",
            "status": "Press Button To View Images",
            "find_image": True,
            "generate_text":True,
            "wordcount": countword
        }                
    
    elif remPunc == 'removepunc':
        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations",
            "analyze_text":True,
            "wordcount": countword
        }
    elif cap == "capitalize":
        analyzed_text = djText.capitalize()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize",
            "analyze_text":True,
            "wordcount": countword
        }

    elif small == "toSmall":
        analyzed_text = djText.lower()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "To Smallercase",
            "analyze_text":True,
            "wordcount": countword
        }

    elif upper == "toUpper":
        analyzed_text = djText.upper()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "To Uppercase",
            "analyze_text":True,
            "wordcount": countword
        }
    elif Links == "Links":
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
