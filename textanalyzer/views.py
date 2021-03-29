from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.utils.html import format_html 
from django.template.loader import get_template
import string
import re
import requests
import json
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import random
import textwrap
from PyDictionary import PyDictionary
from textblob import TextBlob
import random
from gingerit.gingerit import GingerIt
from pyyoutube import Api
from .models import *
from xhtml2pdf import pisa
from django.views.generic import ListView
from .models import Pdf
from wordcloud import WordCloud,STOPWORDS
import io
from io import BytesIO
import urllib,base64
from date_extractor import extract_dates
import matplotlib.pyplot as plt


nltk.download('stopwords')
nltk.download('punkt')

#Api key for the meriam-webster api
api_key = "e7aa870d-ee6d-482c-a437-eb6bb0bcb9c1"


class PdfListView(ListView):
    model = Pdf
    template_name = 'analyze.html'

def render_pdf_view(request):
    template_path = 'pdf.html'
    data = request.session['user-input']
    context = {'myvar': data}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def index(request):

    return render(request, 'home.html')

def about(request):

    api_url='https://api.github.com/repos/rockingrohit9639/TextAnalyzer/contributors'

    response = requests.get(api_url).json()

    context = {
        "userData": response
    }

    return render(request, 'about.html', context)

def youtube(request):
    api=Api(api_key="AIzaSyDHAS3sDLVtUqM1vx-kxykrBHMVSi0BLJI")
    query = request.session['user-input']
    res=api.search_by_keywords(q=query,search_type=["channel"],count=25,limit=8)
    res=res.to_dict()
    res_items=res["items"]
    result=[]

    for data in res_items:
        temp={
        "channel_name":data["snippet"]["title"],
        "channel_url":"https:/www.youtube.com/channel/"+str(data["snippet"]["channelId"]),
        "channel_logo":data["snippet"]["thumbnails"]["default"]["url"]
        }

        result.append(temp)

    context = {
        "result": result,
        "text":query
    }

    return render(request, 'youtube.html', context)

def searchBook(request):
    GOOGLE_BOOKS_API_KEY="AIzaSyDmymOgoPKQZfhMmd3gd9Be-mM6cb8okeM"
    query = request.session['user-input']
    payload = {
        "key": GOOGLE_BOOKS_API_KEY,
        "maxResults": 6,
        "q": query,
    }
    
    resp = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload).json()
    res_items = resp["items"]
    arr=[]

    
    for data in res_items:
        try:
            temp={
            'title':data["volumeInfo"]["title"],
            'link':data["volumeInfo"]["infoLink"],
            'description_text':"".join(data["volumeInfo"]["description"].split(".")[0]),
            'thumbnail':data["volumeInfo"]["imageLinks"]["smallThumbnail"],
            }
        except:
            temp={
            'title':data["volumeInfo"]["title"],
            'link':data["volumeInfo"]["infoLink"],
            'description_text':"Description Not Available",
            'thumbnail':data["volumeInfo"]["imageLinks"]["smallThumbnail"],
            }

        arr.append(temp)

    context = {
        "result": arr,
        "text":query
    }

    return render(request, 'books.html', context)
    
def articles(request):
    Base_string = "https://medium.com/tag/"
    query = request.session['user-input']
    url=Base_string + query
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    logo=[]
    writer=[]
    publisher=[]
    title=[]
    link=[]

    start = soup.find_all('div',class_='streamItem streamItem--postPreview js-streamItem')
    for span in start:
        start1=span.find_all('img')[0]['src']
        logo.append(start1)
        start2=span.find_all('div',class_='postMetaInline postMetaInline-authorLockup ui-captionStrong u-flex1 u-noWrapWithEllipsis')
        for span2 in start2:
            start3=span2.find_all('a')[0].text
            writer.append(start3)
            start4=span2.find_all('a')[1].text
            publisher.append(start4)
        start5 = span.find_all('h3',class_='graf graf--h3 graf-after--figure graf--title')
        for span2 in start5:
            start6=span2.text.replace("\xa0",' ')
            title.append(start6)
        start7=span.find_all('a')[3]['href']
        link.append(start7)

    myDict={"title":[],"writer":[],"publisher":[],"logo":[],"link":[]}
    myDict['title'].extend(title)
    myDict['writer'].extend(writer)
    myDict['publisher'].extend(publisher)
    myDict['logo'].extend(logo)
    myDict['link'].extend(link)

    arr2 = []
    for i in range(0,7):
        try:
            temp = {
            "title": myDict["title"][i],
            "writer": myDict["writer"][i],
            "publisher": myDict["publisher"][i],
            "logo": myDict["logo"][i],
            "link":myDict["link"][i]
           }

        except:
            temp = {
            "title": "Not Available",
            "writer": " ",
            "publisher":" ",
            "logo": " ",
            "link":" "
           }

        arr2.append(temp)

    context = {
        "result": arr2,
        "text":query
    }

    return render(request, 'articles.html', context)


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


    
def get_words_dict(text):
    words_raw = text.split()
    words = {}
    for word in words_raw:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1

    return {key: value for key, value in sorted(words.items(), key=lambda item: item[1], reverse=True)}

def format_spaces(string1, string2, total_chars=40, min_spaces=1):
    num_spaces = total_chars - (len(str(string1)) + min_spaces)
    if num_spaces < min_spaces:
        num_spaces = min_spaces

    return str(string1) + " " * num_spaces + str(string2)

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
    Grammar=request.POST.get('option','grammar')
    Channel=request.POST.get('option','suggest_youtube')
    books=request.POST.get('option','suggest_books')
    replace_input = request.POST.get("other")
    
    if len(djText)==0:
        context = {
            'emptyText': True
        }
        return render(request, 'index.html', context)

    articles=request.POST.get('option','suggest_articles')
    lemmitizer=request.POST.get('option','grammar')
    start_pdf=request.POST.get('option','generate_pdf')
    replace_text = request.POST.get('option', 'replace')
    Word_cloud=request.POST.get('option','wordcloud')
    Date=request.POST.get('option','date')
    Word_frequency=request.POST.get('option','word_frequency')



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
        
    elif Grammar=="grammar":
        parser = GingerIt()
        result = parser.parse(djText)
        final=result["result"]

        if final=='':
            final="Please write some text to check grammar"

        result = {
            "analyzed_text": final,
            "grammar":djText,
            "purpose": "Spelling & Grammar Check",
            "analyze_text":True,
            "wordcount": countword
        }

    elif lemmitizer=="lemmitize":
        wordnet_lemmatizer = WordNetLemmatizer()
        tokenization = nltk.word_tokenize(djText)
        count=True
        for w in tokenization:
            k=wordnet_lemmatizer.lemmatize(w,pos ="v")
            if w!=k:
                result="{} -> {}".format(w, wordnet_lemmatizer.lemmatize(w,pos ="v"))
                count=False
        if count==True:
            final="No need for lemmatization"
        if count==False:
            final="(Original word) - > (Lemmatized word)"
       
        result = {
            "analyzed_text": result,
            "highlight":final,
            "purpose": "Lemmatization of text",
            "analyze_text":True,
            "wordcount": countword
        }


    elif Channel=="suggest_youtube":
        request.session['user-input']=djText
        result = {
            "analyzed_text": djText,
            "purpose":"Suggest youtube channels",
            "status": "Press Button To View Channel links",
            "find_channel": True,
            "generate_text":True,
            "wordcount": countword
        }    

    elif books=="suggest_books":
        request.session['user-input']=djText
        result = {
            "analyzed_text": djText,
            "purpose":"Search Books",
            "status": "Press Button To View Books",
            "find_books": True,
            "generate_text":True,
            "wordcount": countword
        }    

    
    elif articles=="suggest_articles":
        request.session['user-input']=djText
        result = {
            "analyzed_text": djText,
            "purpose":"Search Articles",
            "status": "Press Button To View Articles",
            "find_articles": True,
            "generate_text":True,
            "wordcount": countword
        } 

    elif start_pdf=="generate_pdf":
        request.session['user-input']=djText
        result = {
            "analyzed_text": "Check Your Pdf",
            "purpose":"Generate Pdf",
            "status": "Press Button To View Pdf",
            "make_pdf": True,
            "generate_text":True,
            "wordcount": countword
        } 
        
    elif replace_text == "replace":
        final_text = re.sub(word_to_find, replace_input, djText)
        result = {
            "analyzed_text": final_text,
            "purpose": "Replacemet of text in sentence",
            "analyze_text":True,
            "wordcount": countword
        }
        
    elif Word_cloud=="wordcloud":
        cloud=WordCloud(background_color="white",max_words=200,stopwords=set(STOPWORDS))
        wc=cloud.generate(djText)
        buf=io.BytesIO()
        wc.to_image().save(buf,format="png")
        data=base64.b64encode(buf.getbuffer()).decode("utf8")
        final="data:image/png;base64,{}".format(data)

        result = {
        "analyzed_text":" ",
        "purpose":"Wordcloud",
        "my_wordcloud": final,
        "generate_text":True,
        "wordcount": countword
        } 
    
    elif Date=="date":
        final=extract_dates(djText)
        final_text=final[0].date()

        result = {
            "analyzed_text": final_text,
            "purpose": "Extract Dates from text",
            "analyze_text":True,
            "wordcount": countword
        }
        
    elif Word_frequency=="word_frequency":
        input_text = djText.replace("\n", " ")
        djText = input_text.lower()

        words_dict = get_words_dict(djText)
        # create graph
        if len(words_dict)>10:
            k=10
        else:
            k=len(words_dict)

        y_pos = range(0, k)
        bars = []
        height = []
        count=0

        # print and save values to graph
        format_spaces("word", "occurrences")
        for word_str, word_amount in words_dict.items():
            format_spaces(word_str, word_amount)
            count+=1
            if count<=10:
                bars.append(word_str)
                height.append(int(word_amount))
            else:
                pass

        # # Create bars
        plt.bar(y_pos, height)

        # Create names on the x-axis
        plt.xticks(y_pos, bars, size=9)

        plt.xticks(rotation='horizontal')
        plt.ylabel('Word Frequency',fontsize=12,labelpad=10)
        plt.xlabel('Words',fontsize=12,labelpad=10)

        fig=plt.gcf()

        buf=BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        data=base64.b64encode(buf.read())
        uri=urllib.parse.quote(data)
        final="data:image/png;base64,{}".format(uri)

        result = {
            "analyzed_text": " ",
            "purpose": "Word Frequency for every word in text",
            "bar_graph": final,
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


def contact(request):
    if request.method=="POST":
        name=request.POST['Name']
        email=request.POST['Email']
        message=request.POST['Message']
        user = User_profile.objects.create(name=name,email=email,message=message)
        user.save()
    return render(request,"home.html")

