from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from . import models
import os, sys
import json
import time
import VoiceAutoScore
import difflib

# Create your views here.
def index(request):
    return render(request, 'myapp/index.html')

def upload_action(request):
    if request.method == 'POST':
        start = time.time()
        media = request.FILES.get('testmp3')    # get mp3 file
        if not media:   # judge the media if existence
            return JsonResponse({'result':440, 'sucess':False, 'msg':'You must select a file upload!'})
        ansid = request.POST['ansID']   # get ansid
        media_size = media.size
        if media_size == 0: # judge the size if zero
            return JsonResponse({'result':441, 'sucess':False, 'msg':'You have upload a zero size file!'})

        medianame = os.path.join(settings.MEDIA_ROOT, media.name)
        with open(medianame, 'wb') as f:
            for fmp3 in media.chunks():
                f.write(fmp3)

        # data = VoiceAutoScore.collect_read_feature(medianame, ansid, False)   #Score function
        # data = VoiceAutoScore.collect_read_fast_feature(medianame, ansid)
        # pred = VoiceAutoScore.predict(data,"read.feature","read.model")
        # pred = str(round(pred,2))
        # print("pred:{}".format(pred))
        pred = 3.72

        # recoginze text
        spltfile = os.path.splitext(medianame)    # split medianame file
        if spltfile[1] == ".mp3":
            regname = spltfile[0] + "_recognition.txt"  # recognize text
        with open(regname, 'r') as regf:
            reglines = regf.read()
        new_rglines = reglines[13:].strip()
        spreglines = new_rglines.split(' ')
        newsplines = []
        for regline in spreglines:
            if regline != '<UNK>':
                newsplines.append(regline)
        newsplines = " ".join(newsplines)
        new_reglines = newsplines.lower() 
        # print(newsplines)

        # standard 
        stdname = 'mp3_read_' + ansid + '.txt.train'    # standard text
        with open(os.path.join("lm_txt", stdname), 'r') as stdf:
            stdlines = stdf.read()
        new_stdlines = stdlines[13:].strip()
        new_stdlines = new_stdlines.lower()

        end_stdwords,end_regwords,end_std_dict,end_reg_dict = find_difword(new_stdlines, new_reglines)      # compare 2 text function

        openmp3name = "http://192.168.1.103:9001/" + media.name     # share the filepath

        stop = time.time()
        end = stop - start
        # print("--------------------- Spend %s seconds --------------------" % end)
        endtime = str(round(end,3)) + '秒'

        return render(request, 'myapp/upReturn.html', {'end_stdwords': end_stdwords, 'end_regwords': end_regwords, 'end_std_dict': end_std_dict, 'end_reg_dict': end_reg_dict, 'openmp3name': openmp3name, 'pred': pred, 'endtime': endtime })
    else:
        return JsonResponse({'result': 404, 'sucess': False, 'msg': 'request.method is not POST then upload falid!!!'})

# compare 2 text then mark the defferent
def find_difword(stdwdstr, regwdstr):
    # print(stdwdstr)
    # print()
    # print(regwdstr)
    # print()

    lines1 = stdwdstr.split(' ')
    lines2 = regwdstr.split(' ')

    hd = difflib.ndiff(lines1, lines2)
    cplists = list(hd)

    # print(lines1)
    # print()
    # print(lines2)
    # print()
    # print(cplists)


    templine1 = []
    templine2 = []
    line1_dict = {}
    line2_dict = {}
    count = 0
    for cpline in cplists:
        count += 1
        if cpline[0] == ' ':
            templine1.append(cpline[2:])
            templine2.append(cpline[2:])
            line1_dict[count] = cpline[2:]
            line2_dict[count] = cpline[2:]
        elif cpline[0] == '-':
            # lines1.remove(cpline[2:])
            templine1.append('<' + cpline[2:] + '>')
            line1_dict[count] = cpline[2:]
        elif cpline[0] == '?':
            pass
            # print(cpline[2:])
        else:
            # lines2.remove(cpline[2:])
            templine2.append('<' + cpline[2:] + '>')
            line2_dict[count] = cpline[2:]
            
    return templine1,templine2,line1_dict,line2_dict
    # print(templine1)
    # print(templine2)