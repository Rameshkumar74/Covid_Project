from turtle import width
from flask import Flask,render_template,request,render_template_string
import sqlite3 as sql
app =Flask(__name__)

# Created database
conn = sql.connect('covid.db')
print("Opened Created")
conn.execute('''CREATE TABLE IF NOT EXISTS covid
             (aadhar INT PRIMARY KEY NOT NULL,
             name VARCHAR (255) NOT NULL,
             email VARCHAR(255) NOT NULL,
             age INT NOT NULL,
             doses INT);''')
print("Created table successfully")

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_person():
    return render_template("covid.html")

@app.route ("/addrec",methods = ['POST','GET'])

def addrec():
     if request.method=='POST':
        try:
            aadhar=request.form['aadhar']
            name=request.form['name']
            email=request.form['email']
            age=request.form['age']
            doses=request.form['doses']
            # connect to sqlite3 and execute the record
            print("printed")

            with sql.connect("covid.db") as con:
                cur=con.cursor()
                
                cur.execute("INSERT INTO covid values(?,?,?,?,?)",(aadhar, name, email, age, doses))
                
                con.commit()
                msg = ("Registerd your Vaccition Form")
        except:
            con.rollback
            msg=("Error in Registering your Form , Kindly fill with correct detail")
            print("failed")

        finally:
            con.close()
            return render_template("result.html",msg=msg)
               

@app.route("/list")
def list():
    con = sql.connect("covid.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from covid;")

    rows  = cur.fetchall()
    return render_template("list.html", rows = rows)

@app.route('/available_doses')
def available_doses():
    #Available doses are fetched from a database 
    available_doses = [
        {'vaccine': 'COVID-19 Vaccine', 'doses': 1000},
        {'vaccine': 'Flu Vaccine', 'doses': 500},
        {'vaccine': 'Tetanus Vaccine', 'doses': 300},
    ]
    return render_template('available_doses.html', available_doses=available_doses)


#########################################################################################
# Creating map folium for loactions
import folium

@app.route('/out')
def place():
    print("User entered")
    #Create a map object
    mapobj1 = folium.Map(location=[12.969347306502671, 77.6045036315918], zoom_start=13)
    
    #adding acircle in the map
    folium.Circle(radius=3000,location=[12.969347306502671, 77.6045036315918]).add_to(mapobj1)
    folium.Circle(radius=2000,location=[13.011080746321138, 77.5837326049804]).add_to(mapobj1)
    folium.Circle(radius=4000,location=[12.97269293084298, 77.5349807739258]).add_to(mapobj1)
    folium.Circle(radius=2000,location=[12.965876173694733, 77.6770305633545]).add_to(mapobj1)
    
       
    #addinag a marker in the object
    folium.Marker([12.950279142889631, 77.59641107611252],tooltip= "Apollo Hospital", popup = "Apollo Hospital" ).add_to(mapobj1)
    folium.Marker([12.965766533632836,77.61102505351946],tooltip="Command Hospital", popup = "Command Hospital").add_to(mapobj1)
    folium.Marker([12.984212075924479, 77.60435766874234],tooltip="Global Hospital", popup = "Global Hospital").add_to(mapobj1)
    folium.Marker([12.96828624736315,77.59507127622405], tooltip="Ramani Hospital",popup = "Ramani Hospital").add_to(mapobj1)
    folium.Marker([13.005369479088289,77.578899322768495],tooltip="BOMMA Hospital", popup = "BOMMA HOSPITAL").add_to(mapobj1)
    folium.Marker([13.016491905098967,77.59739581459036],tooltip="Blue Hospital",popup = "Blue HOSPITAL").add_to(mapobj1)
    folium.Marker([12.977288468840992,77.54549451864092],tooltip="Saikrupa Hospital", popup = "Saikrupa Hospital").add_to(mapobj1)
    folium.Marker([12.958534940741258, 77.55355061059885],tooltip="Maruthi Hospital", popup = "Maruthi Hospital").add_to(mapobj1)
    folium.Marker([12.977372151295384, 77.52425138529603],tooltip="Sumathi Hospital", popup = "Sumathi HOSPITAL").add_to(mapobj1)
    folium.Marker([12.960853004829492, 77.53137533165584],tooltip="Shobha Hospital",popup = "Shobha Hospital").add_to(mapobj1)
    folium.Marker([12.99347163064307, 77.53884259799882],tooltip="Supriya Hospital",popup = "Supriya HOSPITAL").add_to(mapobj1)
    folium.Marker([12.968840071251766, 77.50146333477318],tooltip="Sri Ram Hospital", popup = "Sri Ram HOSPITAL").add_to(mapobj1)
    folium.Marker([12.998062398397604, 77.5932428139599],tooltip="CHM Hospital",popup = "CHM HOSPITAL").add_to(mapobj1)
    folium.Marker([12.970308116750354, 77.68225906599645],tooltip="Sakra Hospital",popup = "Sakra HOSPITAL").add_to(mapobj1)
    folium.Marker([12.959814511171112, 77.66822245224236],tooltip="Manipal Hospital", popup = "Manipal HOSPITAL").add_to(mapobj1)
    
       
    #render the map object
    mapobj1.get_root().render()
    
    #derive the script and style tags to be renderd in html head
    header = mapobj1.get_root().header.render()

    #to get the derived div tag to be rendered i the HTNL body
    body_html = mapobj1.get_root().html.render()

    #derive the JS to be rendered in the HTML body
    script = mapobj1.get_root().script.render()

    return render_template_string("""
    <!DOCUTYPE html>
    <html>
        <head>
        {{header|safe}}
        </head>
        <body>
            {{body_html|safe}}
            <script>
             {{script|safe}}                     
            </script>
        </body>
    </html>
    """,header=header,body_html=body_html,script=script)

if __name__ =="__main__":
    app.run(debug=True)
    



