import re

def parse_html_string(html_string):
    #using re library to get all tags
    tags = re.findall(r'<[^>]+>', html_string)

    #String variable used to concatenate parsed tag
    parsed_tag=""

    #Check every tag
    for tag in tags:
        #condition used to get only the start of the tag, for example "span" from <span class="time">
        if " " in tag:
            tag = tag.replace(tag,tag.split(" ")[0])
        #condition used to get only start tag like <span>
        if "/" not in tag:
            tag=tag.split("<")[1].split(">")[0]
            parsed_tag+=f"{tag}+("
        #condition used to get only end tag like </span>
        else:
            parsed_tag+=")"