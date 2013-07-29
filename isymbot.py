import urllib, string, isymmarkov

def extract_posts(pages):
    '''
    Extracts ISYM posts from raw HTML
    '''
    text = ""
    for i in range(2,pages):
        raw = urllib.urlopen("http://isawyou.mit.edu/index.php?page=" + str(i))
        line = raw.readline()
        while line != '</html>\n':
            line = raw.readline()
            if line == '    <div class="entry"><p>\n':
                line = raw.readline()
                while line != '    </p></div>\n':
                    line = line.strip(" \n")
                    line = line.strip("\r")
                    line = line.strip("<br />")
                    text += line + " "
                    line = raw.readline()
                    
    text = text.replace("&quot;", "")
    text = text.replace("I saw you", "")
    return text

def write_isym_text(target="isymbot_text.txt", pages=30):
    '''
    Writes ISYM text to a target file.
    '''
    f = open(target, 'w')
    f.write(extract_posts(pages))
    f.close

def generate_isym(source="isymbot_text.txt", chain_length=3, size=25):
    '''
    Generates ISYM post
    '''
    isympost = isymmarkov.ISYMMarkov(open(source, "r+"), chain_length)
    return isympost.generate_markov_isym(size)

if __name__ == "__main__":
    print generate_isym()
