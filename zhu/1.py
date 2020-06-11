import re
import time
import requests
import os

url = 'http://comic3.ikkdm.com/comiclist/2160/'
data = requests.get(url)
data = data.text.encode('ISO-8859-1').decode('gbk')

href = re.findall("<[aA] href='(/comiclist/2160/.*?)/1.htm'.*?>(.*?)</[Aa]>", data)

a = []
b = []
urls = []
paths = []

a = [i[0] for i in href]
b = [i[1] for i in href]
urls = ["http://comic3.ikkdm.com" + link for link in a]
paths = [d for d in b]

for i in range(105,len(a)):
    paths[i] = paths[i].replace(" ", "_")
    os.system('mkdir ' + paths[i])

    # url = 'http://comic3.ikkdm.com/comiclist/2160/68767'
    url = urls[i]
    content = requests.get(url + '/1.htm')
   
    if(content.status_code == 404):
        print(paths[i]+"--->404")
        continue
        
    content = content.text.encode('ISO-8859-1').decode('gbk')
    total = re.search('共(\\d+)页', content)

    for j in range(1, int(total.group(1)) + 1):
        time.sleep(2)
        host = url + '/' + str(j) + '.htm'
        content = requests.get(host)
        content = content.text.encode('ISO-8859-1').decode('gbk')

        image = re.search("(newkuku/20.*?)'>", content)
        img = 'http://s4.kukudm.com/' + image.group(1)

        jpg = requests.get(img)
        jpg = jpg.content

        with open(paths[i] + '/' + str(j) + '.jpg', 'wb') as f:
            f.write(jpg)

        print("finished %d:%d---->%d:%d" % (int(len(a)),int(total.group(1)),int(i),int(j)))
