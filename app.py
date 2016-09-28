from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def flat():
  import random
  r = random.random()
  return render_template('flat.html', coordinates=r)

@app.route('/pyramid')
def pyramid():
  return 'pyramid!'

@app.route('/about')
def about():
  return 'about!'