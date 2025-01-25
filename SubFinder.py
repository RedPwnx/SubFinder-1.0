import os,requests,subprocess,colorama,sys
from datetime import datetime
import json
import configparser
import random
from time import sleep
config = configparser.ConfigParser()
if os.path.exists('config.ini') == False:
   with open('config.ini','x') as configg:
      configg.write('[options]\n')
      configg.write('webhook = \n')
      configg.write('custom_subdomainlist = \n')
      configg.write('random_domains = True\n')
      configg.close()
config.read('config.ini')
randomains = config.getboolean('options','random_domains')
# --------------------- [ Webhook ] --------------------- #
class DiscordWebhooks:
  def __init__(self, webhook_url, **kwargs):
    # Constructor
    self.webhook_url = webhook_url
    self.content = kwargs.get('content')

    # Generic Embed Data

    # Optional Values
    self.title = None
    self.description = None
    self.url = None
    self.color = None
    self.timestamp = None
    self.author_name = None
    self.author_url = None
    self.author_icon = None
    self.image = None
    self.thumbnail_url = None
    self.footer_text = None
    self.footer_icon = None

    # Fields Array
    self.fields = []

  def set_content(self, **kwargs):
    """
      Sets generic data on the embed object.
    """
    self.content = kwargs.get('content')
    self.title = kwargs.get('title')
    self.description = kwargs.get('description')
    self.url = kwargs.get('url')
    self.color = kwargs.get('color')
    self.timestamp = kwargs.get('timestamp')

  def set_image(self, **kwargs):
    """
      Sets an image on the embed object.
    """
    self.image = kwargs.get('url')

  def set_thumbnail(self, **kwargs):
    """
      Sets a thumbnail on the embed object.
    """
    self.thumbnail_url = kwargs.get('url')

  def set_author(self, **kwargs):
    """
      Sets the author on the embed object.
    """
    self.author_name = kwargs.get('name')
    self.author_url = kwargs.get('url')
    self.author_icon = kwargs.get('icon_url')

  def set_footer(self, **kwargs):
    """
      Sets the footer on the embed object.
    """
    self.footer_text = kwargs.get('text')
    self.footer_icon = kwargs.get('icon_url')

  def add_field(self, **kwargs):
    """
      Adds a field to the embed object.
    """
    field = {
      'name': kwargs.get('name'),
      'value': kwargs.get('value'),
      'inline': kwargs.get('inline', False)
    }

    self.fields.append(field)

  def format_payload(self):
    """
      Formats the data into a JSON object so it can be pushed
      as a payload to Discord.
    """
    # Initializes the default payload structure.
    payload = {}
    embed = {
      'author': {},
      'footer': {},
      'image': {},
      'thumbnail': {},
      'fields': []
    }

    # Attaches data to the payload if provided.
    if self.content:
      payload['content'] = self.content

    if self.title:
      embed['title'] = self.title

    if self.description:
      embed['description'] = self.description

    if self.url:
      embed['url'] = self.url

    if self.color:
      embed['color'] = self.color

    if self.timestamp:
      embed['timestamp'] = self.timestamp

    if self.author_name:
      embed['author']['name'] = self.author_name

    if self.author_url:
      embed['author']['url'] = self.author_url

    if self.author_icon:
      embed['author']['icon_url'] = self.author_icon

    if self.thumbnail_url:
      embed['thumbnail']['url'] = self.thumbnail_url

    if self.image:
      embed['image']['url'] = self.image

    if self.fields:
      embed['fields'] = self.fields

    if self.footer_icon:
      embed['footer']['icon_url'] = self.footer_icon

    if self.footer_text:
      embed['footer']['text'] = self.footer_text

    # If the embed object has content it gets appended to the payload
    if embed:
      payload['embeds'] = []
      payload['embeds'].append(embed)

    return payload

  def send(self):
    """
      Makes a POST request to Discord with the message payload.
    """
    payload = self.format_payload()

    # Makes sure that the required fields are provided before
    # sending the payload.
    if not self.webhook_url:
      print ('Error: Webhook URL is required.')

    elif not payload:
      print ('Error: Message payload cannot be empty.')

    else:
      try:
        request = requests.post(self.webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})

        request.raise_for_status()

      except requests.exceptions.RequestException as error:
        print('Error: %s' % error)
# --------------------- [ Subdomain Checker ] --------------------- #
colorama.init(autoreset=True)
g = colorama.Fore.GREEN
r = colorama.Fore.RED
w = colorama.Fore.LIGHTBLACK_EX
cc = [colorama.Fore.YELLOW,colorama.Fore.RED,colorama.Fore.BLUE,colorama.Fore.LIGHTCYAN_EX,colorama.Fore.CYAN]
c = random.choice(cc)

def httproxies():
    url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    r1 = requests.get(url)
    if r1.ok:
       global proxies
       proxiesInit = r1.text
       proxies = proxiesInit.splitlines()
       for proxy in proxies:
          return proxy
   
def save(subdomain,domain):
    with open(f'{domain}.txt', 'a') as subfile:
        subfile.write(subdomain + "\n")
def check(protocol,domain,current_subdomainslist):
    webhookx = config.get('options','webhook', fallback="")
    s1 = requests
    request2get_subdomins = s1.get(current_subdomainslist)
    if request2get_subdomins.ok:
        subdomainsInit = request2get_subdomins.text
        subdomains = subdomainsInit.splitlines()
    checkdDomain = 0
    errdomains = 0
    for x in range(len(subdomains)):
        try:
            if randomains == True:
              subdomain = random.choice(subdomains)
            else:
              subdomain = subdomains[x]
            domain2check = protocol + subdomain + '.' + domain
            currentdomain = subdomain + '.' + domain
            r1 = s1.get(domain2check)
            if r1.ok:
              if currentdomain not in r1.url:
                  if webhook_status == "True":
                    print(f"{g}[OK] {domain2check}, Notes:{r} The domain redirects -> {r1.url}!")
                    webhook = DiscordWebhooks(webhookx)
                    webhook.set_author(name='Subdomain Checker', url='https://discord.gg/byt')
                    webhook.set_content(description=f"<a:1043627205898539088:1124071467248799755> [OK] Subdomin Found\n<:White1:1259079719723204671> [Notes]: The domain redirects you!\n<:White52:1259079401547632693> [Subdomain]: {domain2check}", color=0xFF0000)
                    webhook.set_footer(text='Ghostbyte Team', icon_url='https://cdn.discordapp.com/icons/1249113251006906430/714a93234962d8c11100e3826916767f.webp')
                    webhook.send()
                  else:
                    print(f"{g}[OK] {domain2check}, Notes:{r} The domain redirects -> {r1.url}!")
                  save(domain2check,domain)
              else:
                  if webhook_status == "True":
                    print(f'{g}[OK] {domain2check}!')
                    webhook = DiscordWebhooks(webhookx)
                    webhook.set_author(name='Subdomain Checker', url='https://discord.gg/byt')
                    webhook.set_content(description=f"<a:1043627205898539088:1124071467248799755> [OK] Subdomin Found\n<:White52:1259079401547632693> [Subdomain]: {domain2check}", color=0xFF0000)
                    webhook.set_footer(text='Ghostbyte Team', icon_url='https://cdn.discordapp.com/icons/1249113251006906430/714a93234962d8c11100e3826916767f.webp')
                    webhook.send()
                  else:
                    print(f'{g}[OK] {domain2check}!')
                  save(domain2check,domain)
              checkdDomain += 1
              os.system(f'title SubFinder 1.0 - Domain: {domain} - Found subdomains: {checkdDomain}')
            elif r1.status_code == 404:
              errdomains += 1
              os.system(f'title SubFinder 1.0 - Domain: {domain} - Found subdomains: {checkdDomain} - Failed Subdomains {errdomains}')
        except requests.exceptions.Timeout as timeouterr:
                print(f'{r}[!] Timeout: {timeouterr}')
        except requests.exceptions.RequestException as err:
            pass
        except requests.exceptions.HTTPError as httperr:
            pass

    
def clear():
   os.system('cls' if os.name == 'nt' else 'clear')
def main():
    clear()
    os.system(f'title SubFinder 1.0 - Main Menu')
    global webhook_status
    webhook_status = "False"
    webhookconf = config.get('options','webhook',fallback="false")
    if webhookconf != "" or "https://" in webhookconf:
      webhookCheck = requests.get(config.get('options','webhook'))
      if webhookCheck.status_code == 404:
        config.set('options','webhook','')
        with open('config.ini','w') as configg:
            config.write(configg)
      elif webhookCheck.ok:
          webhook_status = f"True"
    config.read('config.ini')
    current_subdomainslist = config.get('options', 'Custom_SubdomainList', fallback="false")

    if current_subdomainslist == "false":
        current_subdomainslist = "https://rentry.co/subdomains/raw"
    elif current_subdomainslist != "false":
       if "http" not in current_subdomainslist:
            print(f"{r}[ERR] This domin list site will not work.")
            print(f"{r}[INF] Auto select default subdomain list..")
            current_subdomainslist = "https://rentry.co/subdomains/raw"
            config.set('options','Custom_SubdomainList','https://rentry.co/subdomains/raw')
            with open('config.ini', 'w') as configg:
              config.write(configg)

    print(f"""\n{c}
    ███████╗██╗   ██╗██████╗ ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝██║   ██║██╔══██╗██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
    ███████╗██║   ██║██████╔╝█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
    ╚════██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
    ███████║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
       Copyrights @Ghostbyte 2024                                                               
          

    {c} Available Options{w}:              {c}Configs{w}:{c}
        {w}[1] {c}Start Tool               {w}[!] {c}Webhook Status: {webhook_status}
                                     {w}[!] {c}Random Subdomains: {randomains}
                                     {w}[!] {c}Current SubdomainsList:{g} {current_subdomainslist}
    
    {w}Notes: {c}To update please take a number, or start tool!
""")
    choice = input(f'{w}[ {c}Input A Choice {w}]:{c} ')
    if choice == "1":
        while True:
            protocol = input(f'{w}[{c} Enter protocol {w}[1]{c} Https{w}, {w}[2] {c}Http ]:{c} ')
            if protocol == "1":
                port = "https://"
                break
            elif protocol == "2":
                port = "http://"
                break
            else:
                print(f"{r}[ERR] Select a number.")
        domain = input(f'{w}[{c} Enter Domain example:{w} google.{c}com {w}]:{c} ')
        if "https://" in domain:
            domain = domain.replace('https://', "")
        if "www." in domain:
            domain = domain.replace('www.', "")

        check(port,domain,current_subdomainslist)
main()
