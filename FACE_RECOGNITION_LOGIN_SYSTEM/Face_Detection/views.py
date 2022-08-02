from django.shortcuts import render
from django.http import HttpResponse, request
import speech_recognition as sr
import webbrowser as wb
from .models import usersearches
from operator import attrgetter
import datetime
from django.db import models, connection
from django.shortcuts import render,redirect
from Face_Detection.detection import FaceRecognition
from .forms import *
from django.contrib import messages
faceRecognition = FaceRecognition()
def home(request):
    return render(request,'faceDetection/home.html')

def register(request):
    if request.method == "POST":
        form = ResgistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            print("IN HERE")
            messages.success(request,"Suceessfully registered")
            addFace(request.POST['face_id'])
            redirect('home')
        else:
            messages.error(request,"Account registered failed")
    else:
        form = ResgistrationForm()
    return render(request, 'faceDetection/register.html', {'form':form})

def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('/')

def login(request):
    face_id = faceRecognition.recognizeFace()
    print(face_id)
    return redirect('greeting',str(face_id))

def Greeting(request,face_id):
    face_id = int(face_id)
    context ={
        'user': UserProfile.objects.get(face_id=face_id)
    }
    return render(request,'faceDetection/greeting.html',context=context)


def home2(request):
    return render(request, 'greeting.html', allDynamicContent())

def allDynamicContent():
    recent_var = []
    i = 0
    for str in sorted(usersearches.objects.all(), key=attrgetter('search_datetime'), reverse=True):
        if i < 10:
            recent_var.append(str.search_input)
        i += 1
    recent_searches = recent_var
    return {'recent_searches': recent_searches}

# to receive search query in the form of text
def text(request,face_id):
    search_string = request.POST['TextInput']
    textToWeb(search_string)
    return render(request, 'greeting.html', allDynamicContent())


# to receive audio and converting it into text
def speech(request,face_id):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        output = r.recognize_google(audio)
    except:
        pass
    '''except sr.UnknownValueError:
        output = 'Google speech recognition could not understand audio'
    except sr.RequestError as e:
        output = 'Could not request results from google speech recognition service; {0}'.format(e)'''
    textToWeb(output)
    return render(request, 'greeting.html', allDynamicContent())

# to open client's search query in a new tab
def textToWeb(output_str):
    updateDatabase(output_str)
    outputlist = list(output_str.split(' '))
    search_new_str = '+'.join(outputlist)
    searchquery = 'https://www.google.com/search?q=' + search_new_str
    wb.get().open_new_tab(searchquery)
    return

# updating data when search query is passed
def updateDatabase(output_str):
    current_datetime = datetime.datetime.now()
    try:
        delete_existing_obj = usersearches.objects.filter(search_input=output_str)
        delete_existing_obj.delete()
    except Exception:
        pass
    finally:
        new_obj = usersearches(search_input=output_str, search_datetime=current_datetime)
        new_obj.save()
    return