import requests,random,json;from colorama import *
init()
G1 = '\x1b[1;97m'
G2 = '\x1b[38;5;196m'
G3 = '\x1b[1;33m'
G4 = '\x1b[1;96m'
G5 = '\x1b[38;5;8m'
G6 = '\x1b[38;5;48m'
G7 = '\x1b[38;5;47m'
G8 = '\x1b[38;5;49m'
G9 = '\x1b[38;5;50m'
G10 = '\x1b[1;34m'
G11 = '\x1b[38;5;14m'
G12 = '\x1b[38;5;123m'
G13 = '\x1b[38;5;122m'
G14 = '\x1b[38;5;86m'
G26 = '\x1b[1m'
G27 = '\x1b[0m'
G15 = '\x1b[38;5;205m'
G16 = '\x1b[1;92m\x1b[38;5;208m'
G17 = '\x1b[1;92m\x1b[38;5;209m'
G18 = '\x1b[1;92m\x1b[38;5;210m'
G19 = '\x1b[1;92m\x1b[38;5;211m'
G20 = '\x1b[1;92m\x1b[38;5;212m'
G21 = '\x1b[1;92m\x1b[38;5;46m'
G22 = '\x1b[1;92m\x1b[38;5;47m'
G23 = '\x1b[1;92m\x1b[38;5;48m'
G24 = '\x1b[1;92m\x1b[38;5;49m'
G25 = '\x1b[1;92m\x1b[38;5;50m'
cc = set()
def gen(EmailType):
    r1 = requests.get(f'http://185.158.132.66:80/gmail-temp/api-v2-iq/gen={EmailType}').text
    print(f'{G26}{G1}{r1}{G27}')
def message(EmailCheck,whileTrue=False):
    colors = [G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,G13,G14,G15,G16,G17,G18,G19,G20,G21,G22,G23,G24,G25]
    while True:
        r2 = requests.get(f'http://185.158.132.66:80/gmail-temp/api-v2-iq/msg={EmailCheck}')
        try:
            r = r2.json()
        except:
            r = r2.text
        if isinstance(r,dict) and "emails" in r:
            for email in r["emails"]:
                code = email.get("Code")
                if code not in cc:
                    color = random.choice(colors)
                    print(f'\n{G26}{color}{json.dumps(email,indent=4)}{G27}')
                    cc.add(code)
        if not whileTrue:break