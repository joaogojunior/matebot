# coding: utf8
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError

#from django.core.files.base import ContentFile
#from django.core.files.storage import default_storage
#from django.utils.html import escape

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
# import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import models
from django.http import JsonResponse

import speech_recognition as sr

from math import ceil

root_dir="/caminho/ate/local/dos/arquivos/wav"

semaforo = False

#from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse

#dicionario que contem dados da pesquisa com media e desvio padrao de silabas por minuto
#por faixa etária organizados em 12 grupos
pop_idade={'g1':[(2, 6), (145.74, 42.79)], 'g2':[(7, 11), (150.78, 51.03)], 'g3':[(12, 14), (166.6, 50.2)],
           'g4':[(15, 17), (200.4, 48)], 'g5':[(18, 27), (192.67, 53.3)], 'g6':[(28, 37), (215.09, 48.5)],
           'g7':[(38, 47), (224.24, 43.8)], 'g8':[(48, 59), (179.78, 32.99)], 'g9':[(60,69),(216.95, 53.24)],
           'g10':[(70, 79), (201.64, 52.4)], 'g11':[(80, 89), (183.61, 54.56)], 'g12':[(90, 99), (177.34, 50.52)]}

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def logado_index(request):
    global semaforo
    import time
    while semaforo:
        print "esperando semaforo..."
        time.sleep(2)
    semaforo = True
    #secao critica
    file = open('/caminho/ate/matebot/matebotweb/visitas.txt', 'r')
    try:
        visitas = int(file.readline().strip())
    except:
        visitas = 0
    file.close()
    visitas += 1
    file = open('/caminho/ate/matebot/matebotweb/visitas.txt', 'w')
    file.write(str(visitas) + "\n")
    file.close()
    #fim secao critica
    semaforo = False
    return render_to_response('portal/logado.html',{'visitas': visitas}, context_instance=RequestContext(request))

@login_required
def stress_test(request):
    if 'idade' in request.session:
        idade = request.session['idade']
    else:
        idade = ""
    if 'sexo' in request.session:
        sexo = request.session['sexo']
    else:
        sexo = ""
    return render_to_response('portal/stress.html',{'idade': idade, 'sexo': sexo}, context_instance=RequestContext(request))

@login_required
def resultado(request):
    #carrega o nome da sessao
    filename=request.session['filename']
    print ("filename -"), filename

    #cria o objeto do speechrecognition
    r = sr.Recognizer()
    with sr.WavFile(filename) as source:
        tam=source.DURATION
        audio = r.record(source) # read the entire WAV file

    print "instanciou sr"

    erro="OK"
    texto=""
    silabas = []
    vel=0
    
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        texto=r.recognize_google(audio, key="aqui vai a chave do google api key", language = "pt-BR")
        #print("Debug - texto do google: " + texto)
    except sr.UnknownValueError:
        erro="Google Speech Recognition não pode entender o que você disse ... :("
        #print(erro)
    except sr.RequestError as e:
        erro="Não foi possível obter os resultados... :( - {0}".format(e)
        #print(erro)
        
    s = ""
    sil=0
    
    if texto != "":
        #salva na sessao o texto
        request.session['texto']= texto

        # from hyphen.dictools import is_installed, install
        from hyphen import Hyphenator
        
        h_br = Hyphenator('pt_BR', directory='/caminho/ate/matebot/matebotweb/')
        
        palavras=texto.split(" ")
        for palavra in palavras:
            silabas=h_br.syllables(palavra)
            # print (palavra, silabas)
            if len(silabas) == 0:
                s = s + palavra + "-"
                sil+=1
            else:
                s = s + "-".join(silabas) + "-"
                sil=len(silabas)+sil
                        
        # print "lista de silabas -", s
        request.session['silabas'] = s
        request.session['numsil'] = sil
        request.session['tamanho'] = tam
        #velocidade em silabas por minuto
        vel=(sil/tam) * 60
        print "Vel -", vel
        request.session['vel'] = vel
        
    dados = ""

    if texto == "":
        texto = erro
        dados = "Houve um erro no serviço tente novamente mais tarde..."
        #desabilita botao
        btntxt="Desativado"
        return render_to_response('portal/resultado.html',{'tam': ceil(tam),'texto': texto,'total': sil,'vel': round(vel,2),'velocidade': vel,'dados': dados,'btntxt': btntxt},context_instance=RequestContext(request))

    idade = request.session['idade']
    print "idade -", idade

    #iterando o dicionario a procura do grupo da idade
    media=""
    dp=""
    for key in pop_idade:
        idmin, idmax = pop_idade[key][0]
        if int(idmin) <= int(idade) and int(idade) <= int(idmax):
            media, dp = pop_idade[key][1]
            media, dp = float(media), float(dp)
            break

    print "media e dp -", media, dp
    #z critico
    z = (vel - media) / dp

    print "z -", z
    # teste 1
    # h0 a pessoa esta normal
    # h1 a pessoa esta estressada media da amostra maior que da pop
    if z < 1.64:
        #h0 - pessoa nao esta estressada mas testa se esta relaxada
        # teste 2
        # h0 a pessoa esta normal
        # h1 a pessoa esta relaxada media da amostra menor que da pop
        if -1.64 < z:
            #h0 - pessoa normal
            dados = "Você está bem..."
        else:
            #h1 - pessoa relaxada
            dados = "Você está relaxado!"
    else:
        #h1 - pessoa estressada
        dados = "Você está estressado!"

    return render_to_response('portal/resultado.html',{'tam': ceil(tam),'texto': texto,'total': sil,'vel': round(vel,2),'velocidade': vel,'dados': dados},context_instance=RequestContext(request))

@login_required
def processa(request):
    return render_to_response('portal/aguarde.html', context_instance=RequestContext(request))

@login_required
@csrf_protect
def salvar(request):
    if request.method == 'POST':
        if 'rotulo' in request.POST:
            rotulo = request.POST['rotulo']
            #Atualizando objeto Dado...
            #try:
            #    objeto = models.Dado.objects.get(user=request.user)
            #except models.Dado.DoesNotExist:
            #    objeto = None
            #    #print ("o objeto nao existia!")
                
            #if objeto == None:
            #print ("objeto foi none, instanciando um novo...")
            objeto = models.Dado()
            #print ("objeto foi instanciado, agora setando o user...")
            #print ("setando o user...")
            objeto.user = request.user
            # print request.user
            objeto.filename = request.session['filename']
            # print request.session['filename']
            objeto.tamanho = request.session['tamanho']
            # print request.session['tamanho']
            texto = request.session['texto']
            objeto.texto = texto
            # print request.session['texto']
            objeto.numsil = request.session['numsil']
            # print request.session['numsil']
            objeto.silabas = request.session['silabas']
            # print request.session['silabas']
            objeto.vel = request.session['vel']
            # print request.session['vel']
            ip =  get_client_ip(request)
            # print ip
            if ip == "::1":
                ip = "127.0.0.1"
            print "ip do cliente -", ip
            objeto.ipaddr = ip
            import pygeoip
            gi = pygeoip.GeoIP('/home/zuao/git/matebot/matebotweb/GeoLiteCity.dat')
            if ip == '127.0.0.1' or ip.split(".")[:2] == ['192', '168']:
                geo = {'city': u'Recife', 'region_code': u'30', 'area_code': 0, 'time_zone': 'America/Recife', 'dma_code': 0, 'metro_code': None, 'country_code3': 'BRA', 'latitude': -8.050000000000011, 'postal_code': None, 'longitude': -34.900000000000006, 'country_code': 'BR', 'country_name': 'Brazil', 'continent': 'SA'}
            else:
                geo = gi.record_by_addr(ip)
            geotxt=geo['city'] + ", " + geo['country_name']
            print "geo info -", geotxt
            objeto.geo = geotxt
            objeto.latitude = geo['latitude']
            objeto.longitude = geo['longitude']
            print "rotulo -", rotulo
            objeto.rotulo = rotulo
            print "idade -", request.session['idade']
            objeto.idade = request.session['idade']
            print "sexo -", request.session['sexo']
            objeto.sexo = request.session['sexo']

            #analise sentimento no texto
            from textblob import TextBlob as tb
            tblob = tb(texto)
            if tblob.detect_language() != "en":
                try:
                    tblob2 = tb(tblob.translate(to='en').string)
                except:
                    # no caso da traducao falhar passamos o mesmo texto original mesmo (provavelmente a analise de sentimento vai dar 0)
                    # nao é ideal mas melhor que nao tratar a excecao
                    tblob2 = tblob
            polarity = tblob2.sentiment.polarity
            print "polarity -", polarity
            objeto.polarity = polarity

            #print ("salvando objeto...")
            try:
                objeto.save(force_insert=True)
            except Exception, e:
                print "Nao pode escrever no db -", str(e)
                
            return HttpResponse() # if everything is OK
    # nothing went well
    return HttpResponseServerError()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
@csrf_protect
def uploadFile(request):

    import datetime
    #cria um novo nome para o arquivo
    filename = root_dir + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + '.wav'

    #salva filename na sessao
    request.session['filename']=filename

    retvals = {}
    
    message="failure"
    if  (request.method == 'POST'):
        if request.FILES.has_key('file'):
            filelocal = request.FILES['file']
            #print 'file=',filelocal
            with open(filename, 'wb') as dest:
                for chunk in filelocal.chunks():
                    dest.write(chunk)
            #chama rotina de preprocessamento de audio
            audio_pre(filename)
            message="success"
        if 'idade' in request.POST:
            #salva idade na sessao
            request.session['idade'] = request.POST['idade']
        if 'sexo' in request.POST:
            #salva idade na sessao
            request.session['sexo'] = request.POST['sexo']
    retvals['message']= message
    retvals['filename']= filename
    if message == "success":
        print 'success'
        print retvals
        return JsonResponse(retvals)
    else:
        return HttpResponseServerError()

def audio_pre(filename):
    #tenta remover os silencios do inicio e do fim
    #converte para 16Khz mono (wave)
    from pydub import AudioSegment

    #carrega audio do arquivo
    sound = AudioSegment.from_file(filename, format="wav")

    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]

    #re-sampleia para 16Khz
    trimmed_sound = trimmed_sound.set_frame_rate(16000)
    #converte pra mono
    trimmed_sound = trimmed_sound.set_channels(1)
    #re-escreve arquivo
    trimmed_sound.export(out_f=filename, format="wav" )

#metodo para encontrar silencio
def detect_leading_silence(sound, silence_threshold=-35.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms
