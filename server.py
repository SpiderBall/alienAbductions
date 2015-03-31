import psycopg2
import psycopg2.extras

from flask import Flask, render_template, request
app = Flask(__name__)

def connectToAliens():
  connectionString = 'dbname=alien user=alien password=aupass host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database alien")

def connectToDB():
  connectionString = 'dbname=music user=postgres password=post host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def mainIndex():
    return render_template('index.html', selectedMenu='Home')

@app.route('/report', methods=['GET', 'POST'])
def report():
  conn = connectToAliens()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if request.method == 'POST':
    appearance = request.form.getlist('attribute')
    appearanceStr = ', '.join(appearance)
    try:
      cur.execute("""INSERT INTO abductions (first, last, handle,
      month, day, year, city, state, scary, attributes) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
      (request.form['firstname'], request.form['lastname'], 
      request.form['handle'], request.form['month'],
      request.form['day'], request.form['year'],
      request.form['city'], request.form['state'],
      request.form['scary'], appearanceStr))
    except:
      print("Error executing insert")
  conn.commit()
  return render_template('report.html', selectedMenu='Report')

@app.route('/report2', methods=['POST'])
def report2():
  conn = connectToAliens()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    cur.execute("""SELECT * FROM ABDUCTIONS;""")
  except:
    print("Error executing select")
  results = cur.fetchall()
  for r in results:
    print r
  conn.commit()
  return render_template('report2.html', abductions=results)
  
@app.route('/listOfAbductions')
def abductionList():
  conn = connectToAliens()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    cur.execute("""SELECT * FROM ABDUCTIONS;""")
  except:
    print("Error executing select")
  results = cur.fetchall()
  for r in results:
    print r
  conn.commit
  return render_template('abductionList.html', selectedMenu = 'list', abductions=results)

@app.route('/simple')
def simple():
  return render_template('simple.html')

@app.route('/simple2', methods=['POST'])
def simple2():
  return render_template('simple2.html')


@app.route('/simple3')
def simple3():
  return render_template('simple3.html')

@app.route('/simple4', methods=['POST'])
def simple4():
  return render_template('simple4.html', name=request.form['name'])

@app.route('/music')
def showChart():
  """rows returned from postgres are just an ordered list"""
  
  conn = connectToDB()
  cur = conn.cursor()
  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  return render_template('music.html', albums=results)

@app.route('/music2')
def showChartUsingPythonDictionary():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  print results
  return render_template('music2.html', albums=results)


@app.route('/music3', methods=['GET', 'POST'])
def showChartForms():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if request.method == 'POST':
    # add new entry into database
    try:
      cur.execute("""INSERT INTO albums (artist, name, rank) 
       VALUES (%s, %s, %s);""",
       (request.form['artist'], request.form['album'], request.form['rank']) )
    except:
      print("ERROR inserting into albums")
  conn.commit()
  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  for r in results:
    print r['artist']
  conn.commit()
  return render_template('music3.html', albums=results)



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)
