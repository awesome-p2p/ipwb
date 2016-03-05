from surt import surt

import ipfsApi
import json
from pywb.utils.binsearch import iter_exact
from flask import Flask
from flask import Response

app = Flask(__name__)
app.debug = True
#@app.route("/")
#def hello():
#    return "Hello World!"
IP = '127.0.0.1'
PORT = '5001'
IPFS_API = ipfsApi.Client(IP, PORT)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_uri(path):
    global IPFS_API
    (requestedDatetime, requestedUrir) = path.split('/', 1)
    
    # show the user profile for that user
    cdxLine = getCDXLines(surt(requestedUrir), requestedDatetime)
    (surtURI, cdxDatetime, cdxjLine) = cdxLine.split(" ", 2)
    jObj = json.loads(cdxjLine)
    
    payload = IPFS_API.cat(jObj['payload_digest'])
    header = IPFS_API.cat(jObj['header_digest'])

    hLines = header.split('\n')
    hLines.pop(0)
    
    resp = Response(payload)

    for idx,hLine in enumerate(hLines):
      k,v = hLine.split(': ', 1)
      if k.lower() != "content-type":
        k = "X-Archive-Orig-" + k
      resp.headers[k] = v
      
    return resp

def getCDXLines(surtURI, datetime):
  with open('index.cdx', 'r') as cdxFile:
    bsResp = iter_exact(cdxFile, surtURI)
    print bsResp
    cdxLines = []  
    
    count = 0
    while count < 100:
      count += 1

      cdxl = bsResp.next()

      print cdxl
      (uriKey, cdxDatetime, cdxjLine) = cdxl.split(" ", 2)
      if uriKey != surtURI: break
      cdxLines.push((uriKey, cdxDatetime, cdxjLine))
      
    if datetime != '*':
      minTimeDistance = 99999999
      for cdxItems in enumerate(cdxLines):
        print cdxItems
        timeDistance = abs(int(datetime) - int(cdxDatetime))
        if timeDistance <  minTimeDistance:
          minTimeDistance = timeDistance
        
    #cdxLine = bsResp.next()
    
    
    #return cdxLine

    

if __name__ == "__main__":
    app.run()


if __name__ == '__main__':
  main()  