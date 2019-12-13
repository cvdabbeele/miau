from flask import Flask, render_template
import random

app = Flask(__name__)

# list of cat images
images = [
    "https://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-1376-1381846217-0.gif",
    "https://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-29111-1381845968-0.gif",
    "https://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26358-1381845043-13.gif",
    "http://www.catgifpage.com/gifs/284.gif"
]

@app.route('/')
def index():
    f=open("/etc/os-release", "r").read()
    url = random.choice(images)
    return render_template('index.html', url=url, f=f)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
