from django.http import HttpResponse
from django.shortcuts import render
import string

def index(request):

    return render(request, 'index.html')

def analyze(request):
    
    puncts = string.punctuation
    djText = request.POST.get('text', 'default')
    remPunc = request.POST.get('removepunc', 'off')
    cap = request.POST.get('capitalize', 'off')
    small = request.POST.get('toSmall', 'off')
    upper = request.POST.get('toUpper', 'off')
    analyzed_text = ""
    countword = len(djText.split())

    if remPunc == "on" and cap == "on":
        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char

        analyzed_text = analyzed_text.capitalize()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations & Capitalize",
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
            "wordcount": countword
        }

    elif cap == "on" and small == "on":
        analyzed_text = djText
        analyzed_text = analyzed_text.capitalize()
        analyzed_text = analyzed_text.lower()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize & To Small",
            "wordcount": countword
        }

    elif cap == "on" and upper == "on":
        analyzed_text = djText
        analyzed_text = analyzed_text.capitalize()
        analyzed_text = analyzed_text.upper()
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize & To Upper",
            "wordcount": countword
        }
    elif small == "on" and upper == "on":
        analyzed_text = "Text can be smaller or uppercase only."
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Small & Upper",
            "wordcount": countword
        }

    elif remPunc == 'on':
        for char in djText:
            if char not in puncts:
                analyzed_text = analyzed_text + char
        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Remove Punctuations",
            "wordcount": countword
        }
    elif cap == "on":
        analyzed_text = djText.capitalize()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "Capitalize",
            "wordcount": countword
        }

    elif small == "on":
        analyzed_text = djText.lower()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "To Smallercase",
            "wordcount": countword
        }

    elif upper == "on":
        analyzed_text = djText.upper()

        result = {
            "analyzed_text": analyzed_text,
            "purpose": "To Uppercase",
            "wordcount": countword
        }
    else:
        return HttpResponse('''<script type="text/javascript">alert("Please select atleast one option.");</script>''')

    return render(request, 'analyze.html', result)