import re
html = '<html><head><h1>Hi</h1><p>test <span class="time">test</span></p></head></html>'
tags = re.findall(r'<[^>]+>', html)

string=""

for a in tags:
    if " " in a:
        a = a.replace(a,a.split(" ")[0])
    if "/" not in a:
        a=a.split("<")[1].split(">")[0]
        string+=f"{a}+("
    else:
        string+=")"
        #print(a)

print(string)