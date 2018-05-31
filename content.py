import random
import sys
import re
import time
from PyRTF import *

def build_chain(text, chain = {}):
    words = text.split(' ')
    index = 1
    for word in words[index:]:
        key = words[index - 1]
        if key in chain:
            chain[key].append(word)
        else:
            chain[key] = [word]
        index += 1
    
    return chain

def generate_message(chain, count = 10500):
    word1 = random.choice(list(chain.keys()))
    message = word1.capitalize()

    # while len(message.split(' ')) < count:
    while len(message) < count:
        word2 = random.choice(chain[word1])
        word1 = word2
        message += ' ' + word2
    
    return message

def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read().replace('\n\n',' ')
    return contents

def write_file(filename, message):
    with open(filename, "w") as file:
        file.write(message)
             
if __name__ == '__main__':
    creation_time = time.strftime('%x %X')
    FILE = 'output'+str(creation_time).replace(":", "-").replace("/", "-")
    message = read_file("src.txt")
    chain = build_chain(message)
    message = generate_message(chain)
    write_file(FILE, message)    

    title = ''
    index = ['Index\n']
    for l in open(FILE).readlines():
        if l.count(' ') < 10: 
            index.append(l)
            if l.count(' ') > 1 and l.count(' ') < 6:
                title = l
    

    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)


    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append(title)
    section.append(p)

    p = Paragraph( ss.ParagraphStyles.Heading2 )
    p.append(creation_time)
    section.append(p)

    for l in index:
        para_props = ParagraphPS()
        para_props.SetLeftIndent( TabPropertySet.DEFAULT_WIDTH *  3 )
        p = Paragraph( ss.ParagraphStyles.Normal, para_props )
        p.append(l)
        section.append( p )


    for l in open(FILE).readlines():
        p = Paragraph( ss.ParagraphStyles.Normal )
        p.append(l)
        section.append( p )

    DR = Renderer()
    DR.Write(doc, file( FILE+'.rtf', 'w' ))
