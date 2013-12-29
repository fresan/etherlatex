#!/usr/bin/python
#
# Python script that downloads an Etherpad lite document
# and compiles it locally using pdflatex and bibtex. For
# further information see http://pendicular.net/etherlatex.php
#
# Written by Fredrik.Sandin@gmail.com, January 2013.

import urllib2, ast, subprocess, sys

### CONFIGURATION #############

# Etherpad document ID (padID)
doc = "test";
bib = "testbib";

# Target folder where the latex file is to be downloaded and compiled
odr = "/not/in/www/folder/"

# Etherpad url and API Key
url = "http://etherpad.server.se";
key = "EtherpadServerSecretKey";

##############################

# Download document using the etherpad http API (or https if needed)
url1 = ''.join([url, "/api/1.2/getText?apikey=", key, "&padID=%s" % doc]);
text = ast.literal_eval(urllib2.urlopen(url1).read());
text = text["data"];
text = text["text"];
f = open(''.join([odr, doc, ".tex"]), 'w');
f.write(text);
f.close();


# Download bibtex reference file
url2 = ''.join([url, "/api/1.2/getText?apikey=", key, "&padID=%s" % bib]);
text = ast.literal_eval(urllib2.urlopen(url2).read());
text = text["data"];
text = text["text"];
f = open(''.join([odr, doc, ".bib"]), 'w');
f.write(text);
f.close();

# bibtex
p = subprocess.Popen(["bibtex", ''.join([odr, doc])], stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
p.wait();
serr = p.communicate();
f = open(''.join([odr, doc, ".bib.err"]), 'w');
f.write(serr[0]);
f.close();

# pdflatex
p = subprocess.Popen(["pdflatex", "-halt-on-error", "-output-directory", odr, ''.join([odr, doc, ".tex"])], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
retcode = p.wait();
serr = p.communicate();
f = open(''.join([odr, doc, ".err"]), 'w');
f.write(serr[0]);
f.close();

# Exit with return code
sys.exit(retcode);

# EOF
