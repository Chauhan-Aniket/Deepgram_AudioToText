# Create your views here.
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AudioForm
from django.core.files.storage import FileSystemStorage
from deepgram_app.settings import *
# deepgram sdk
from deepgram import Deepgram
import asyncio
import json


class HomePageView(TemplateView):
    template_name = "home.html"


def Audio_upload(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            myfile = request.FILES['record']
            fs = FileSystemStorage()
            uploaded_file_url = fs.url(myfile).replace(
                '%', '_').replace('20', '').replace(' ', '_')
            print(uploaded_file_url)
            asyncio.run(main(uploaded_file_url))
            with open('./audio.json', 'r') as j:
                contents = json.loads(j.read())
            return render(request, 'audio.html', {
                'uploaded_file_url': uploaded_file_url, 'audio_content': contents['results']['channels'][0]
                ['alternatives'][0]['transcript']})
    else:
        form = AudioForm()
    return render(request, 'form.html', {'form': form})


DEEPGRAM_API_KEY = env('DEEPGRAM_API')
MIMETYPE = 'audio/mpeg'


async def main(PATH_TO_FILE):
    # init the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # open audio file
    audio = open('.{}'.format(PATH_TO_FILE), 'rb')
    if MIMETYPE == 'audio/wav':
        source = {'buffer': audio, 'mimetype': MIMETYPE}
    else:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
    response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
    # save it to json
    audio_json = open('./audio.json', 'w')
    audio_json.write(json.dumps(response, indent=2))
