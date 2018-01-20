import requests
import math
import shutil
import sys
import datetime
import time
import winsound
from itertools import zip_longest

# Retrieve terminal dimensions
termcols, termrows = shutil.get_terminal_size()


def PlayNote(note, octave, duration):
    key = 3 + 12 * (4 + octave) + note
    fre = int(2 ** ((key - 49) / 12) * 440)

    winsound.Beep(fre, duration)

def Alarm1():
    PlayNote(1, 1, 500)

def QueryForChange(url, alert=True):
    waitsecs = 3
    dotwaitsecs = 0.5

    initialcontent = requests.get(url).text
    initialtime = datetime.datetime.now()
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

        latestcontent = requests.get(url).text
        elapsedtime = datetime.datetime.now() - initialtime
        elapsedtstr = str(elapsedtime).split('.')[0]

        timeinfostr = 'Elapsed:\t' + elapsedtstr

        return latestcontent == initialcontent

    print('Querying:\t' + url)
    print('Started:\t' + initialtstr)

    while QueryLatest():
        sys.stdout.write('\r' + ' ' * (termcols - 1))
        sys.stdout.write('\r' + timeinfostr + ' ')
        sys.stdout.flush()

        for _ in range(int(waitsecs / dotwaitsecs)):
            time.sleep(dotwaitsecs)
            sys.stdout.write('.')
            sys.stdout.flush()

        time.sleep(waitsecs % dotwaitsecs)

    sys.stdout.write('\n')
    print('The page has changed!')

    if alert:
        Alarm1()


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
    'http://www.math.boun.edu.tr/courses/course/view.php?id=7'
]

websiteoffers.append('... or specify other')

websitechoice = offerthelist(
    'Please select one of the websites below to query for changes:',
    websiteoffers,
    default=1)

if websitechoice == len(websiteoffers) - 1:
    url = input('Specify the website to query: ')
else:
    url = websiteoffers[websitechoice]

QueryForChange(url)
