import requests
from bs4 import BeautifulSoup
import math
import shutil
import sys
import os
from datetime import datetime
import time
from itertools import zip_longest
import json
from random import random

if 'TELEGRAM_CHAT_ID' in os.environ:
    whomstd = os.environ['TELEGRAM_CHAT_ID']
elif len(sys.argv) > 2:
    whomstd = sys.argv[2]
else:
    print("too few arguments and TELEGRAM_CHAT_ID not set")
    quit()

if 'TELEGRAM_TOKEN' in os.environ:
    telegramToken = os.environ['TELEGRAM_TOKEN']
elif len(sys.argv) > 1:
    telegramToken = sys.argv[1]
else:
    print("too few arguments and TELEGRAM_TOKEN not set")
    quit()

def WinSoundPlayer(freq, duration):
    winsound.Beep(freq, duration)

def FallbackSoundPlayer(freq, duration):
    pass

if sys.platform == "win32":
    import winsound
    SoundPlayer = WinSoundPlayer
else:
    SoundPlayer = FallbackSoundPlayer

# Retrieve terminal dimensions
termcols, termrows = shutil.get_terminal_size()


def PlayNote(note, octave, duration):
    key = 3 + 12 * (4 + octave) + note
    fre = int(2 ** ((key - 49) / 12) * 440)

    SoundPlayer(fre, duration)

def Alarm1():
    PlayNote(1, 1, 500)

def AlarmTelegram(website):
    requests.post(url = 'https://api.telegram.org/bot' + telegramToken + '/sendMessage',
            params = {'chat_id': whomstd, 'text': 'It has changed! ' + website})

def QueryForChange(website, alert=True):
    basewaitsecs = 60 * 15
    dots = 100

    def GetContent():
        while True:
            try:
                requesttext = requests.get(website[0]).text
                soup = BeautifulSoup(requesttext, 'html.parser')
                matches = soup(**website[1])
                theobject = matches[website[2]]

                return (theobject.text, datetime.now())
            except:
                pass

    initialcontent, initialtime = GetContent()
    initialtstr = initialtime.strftime('%d %b %Y %H:%M:%S')

    latestcontent = None
    elapsedtime = None
    elapsedtstr = None
    timeinfostr = None

    def QueryLatest():
        nonlocal latestcontent
        nonlocal elapsedtime
        nonlocal elapsedtime
        nonlocal elapsedtstr
        nonlocal timeinfostr

        latestcontent, latesttime = GetContent()
        elapsedtime = latesttime - initialtime
        elapsedtstr = str(elapsedtime).split('.')[0]

        timeinfostr = 'Elapsed:\t' + elapsedtstr

        return latestcontent == initialcontent

    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    print('Querying:\t' + str(website))
    print('Started:\t' + initialtstr)

    while QueryLatest():
        sys.stdout.write('\r' + ' ' * (termcols - 1))
        sys.stdout.write('\r' + timeinfostr + ' ')
        sys.stdout.flush()

        waitsecs = int(basewaitsecs * (1 + random()))
        dotwaitsecs = waitsecs / dots

        for i in range(dots):
            time.sleep(dotwaitsecs)
            sys.stdout.write('.' if i % 10 else i)
            sys.stdout.flush()

        time.sleep(waitsecs % dotwaitsecs)

    sys.stdout.write('\n')
    print('The page has changed!')

    if alert:
        AlarmTelegram(website[0])

###
# Definitions of the offering functions
###


def printlist(offerlist, columncount):
    rowcount = math.ceil(len(offerlist) / columncount)
    columnwid = (termcols - 1) // columncount

    columns = []
    for i in range(columncount):
        start = i * rowcount
        end = start + rowcount
        column = [offer for offer in offerlist[start:end]]

        longestnrwid = len(str(end))
        longestofferwid = max(len(offer) for offer in column)

        for idx, offer in enumerate(column):
            offernr = repr(start + idx + 1).rjust(longestnrwid)
            column[idx] = (offernr + ') ' + offer).ljust(columnwid)[:columnwid]

        columns.append(column)

    rowtuples = zip_longest(*columns, fillvalue='')

    print('\n'.join(''.join(rowtuple) for rowtuple in rowtuples))


def offerthelist(question, offerlist, columncount=1, default=False):
    offerlist = [str(x) for x in offerlist]
    printlist(offerlist, columncount)

    if default:
        question += ' (default: ' + str(default) + ')'

    while True:
        print(question)
        inp = input()

        if inp:
            if inp.isdigit():
                choice = int(inp)
            else:
                continue
        else:
            choice = default

        if 1 <= choice <= len(offerlist):
            break

    return choice - 1


def offeryesno(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    if default is None:
        prompt = " [y/n]"
    elif default in valid:
        prompt = " [Y/n]" if valid[default] else " [y/N]"
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt, end=' ', flush=True)
        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")

################                     ################
################ Program Starts Here ################
################                     ################

print('Welcome to the Website Querying Machine!')

websiteoffers = [
        ('http://www.math.boun.edu.tr/courses/course/view.php?id=7', {'name':'body'}, 0),
        ('https://www.tubitak.gov.tr/tr/destekler/bilimsel-etkinlik/etkinliklere-katilma-destekleri/icerik-2224-a-yurt-disi-bilimsel-etkinliklere-katilimi-destekleme-programi', {'id':'section-content'}, 0)
]

websiteoffers.append('... or specify other')

websitechoice = offerthelist(
    'Please select one of the websites below to query for changes:',
    websiteoffers,
    default=1)

if websitechoice == len(websiteoffers) - 1:
    websiteurl = input('Specify the website to query: ')
    bsquery = input('Specify the BeautifulSoup query to search: ')
    try:
        bsquery = json.loads(bsquery)
    except:
        bsquery = {"name": bsquery}
    index = int(input('Specify the index: '))
    website = (websiteurl, bsquery, index)
else:
    website = websiteoffers[websitechoice]

QueryForChange(website)
