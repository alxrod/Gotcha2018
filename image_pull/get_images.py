from bs4 import BeautifulSoup
import requests
import lxml.html

s = requests.session()
login = s.get('https://mymustangs.milton.edu/student/')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath("//form[@name='LoginForm']/@action")
print(hidden_inputs)
tokens = (hidden_inputs[0].split("?"))[1].split("&")
cfid = tokens[0].split("=")
cftok = tokens[1].split("=")
print(cfid , cftok)
cookies = {'CFID':cfid[1], 'CFTOKEN':cftok[1]}
user = 'Zankner20'
password = '4pcsuqi1'
payload = {'UserLogin_required':'','UserPassword_required'='','UserLogin':user, 'UserPassword':password}
response = s.post('https://mymustangs.milton.edu/student/', cookies = cookies, data=payload)
