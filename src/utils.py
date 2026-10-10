import re



def clean_title(title):

    return re.sub(r"\(\d{4}\)","",title).strip()#.lower()
