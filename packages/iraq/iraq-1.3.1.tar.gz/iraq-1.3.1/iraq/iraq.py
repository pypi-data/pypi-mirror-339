import requests,random,json
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
    url = f'http://185.158.132.66:80/gmail-temp/api-v2-iq/gen={EmailType}'
    response = requests.get(url).text
    print(f'{G26}{G1}{response}{G27}')

def message(EmailCheck, whileTrue=False):
    colors = [
        '\x1b[1;97m', '\x1b[38;5;196m', '\x1b[1;33m',
        '\x1b[1;96m', '\x1b[38;5;48m', '\x1b[38;5;47m'
    ]
    
    while True:
        url = f'http://185.158.132.66:80/gmail-temp/api-v2-iq/msg={EmailCheck}'
        response = requests.get(url)
        
        try:
            data = response.json()
        except:
            data = response.text
        
        if isinstance(data, dict) and "emails" in data:
            for email in data["emails"]:
                code = email.get("Code")
                if code not in cc:
                    color = random.choice(colors)
                    print(f'\n{G26}{color}{json.dumps(email, indent=4)}{G27}')
                    cc.add(code)
        
        if not whileTrue:
            break