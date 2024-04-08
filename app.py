# an object of WSGI application

from datetime import datetime

import pyodbc
from flask import Flask, jsonify, render_template, request, Response
from PyZ3950 import z3950, zoom
from fuzzywuzzy import process

app = Flask(__name__, template_folder="templates")  # Flask constructor

# A decorator used to tell the application
# which URL is associated function
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:aurexdb.database.windows.net;Database=AUREXDB1;Uid=db_su;Pwd={=!Aurexus21!=};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/dbconnect")
def dbConnect():
    # conn_str = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:aurexdb.database.windows.net;Database=AUREXDB1;Uid=db_su;Pwd={=!Aurexus21!=};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    cnxn = pyodbc.connect(conn_str)
    html_content = ""
    if cnxn:
        cursor = cnxn.cursor()
        cursor.execute("SELECT top(10) * FROM HUB_TEST")
        rows = cursor.fetchall()
        
        #for row in rows:
            #return str(row)
        html_content += "<table class='table' style=''>"
        
        # Generate table headers
        #for column in cursor.description:
            #html_content += "<th>" + column[0] + "</th>"
        #html_content += "</tr>"
        
        html_content += "<thead><tr>"
        html_content += "<th>ID</th>"
        html_content += "<th>Image</th>"
        html_content += "<th>Cote</th>"
        html_content += "<th>Localisation</th>"
        html_content += "<th>Numserie</th>"
        html_content += "<th>Serietra</th>"
        html_content += "<th>Articleno</th>"
        html_content += "<th>Action</th>"
        html_content += "</tr></thead>"
        html_content += "<tbody>"
        #for column_name in ['ID', 'Image', 'cote', 'Localisation', 'numserie', 'serietra', 'articleno']:  # Specify the column names you want in the header
            #html_content += "<th>" + column_name + "</th>"
        #html_content += "</tr></thead>"
        
        # Generate table rows
        for row in rows:
            html_content += "<tr>"
            #for value in row:
                #html_content += "<td>" + str(value) + "</td>"
            #html_content += "</tr>"
            row_dict = dict(zip([column[0] for column in cursor.description], row))
            for column_name in ['ID', 'Image', 'cote', 'Localisation', 'numserie', 'serietra', 'articleno']:
                html_content += "<td>" + str(row_dict[column_name]) + "</td>"
            html_content += "<td><button class='btn-sm btn-primary'><i class='fa-solid fa-edit'></i></button></td>"
            html_content += "</tr>"
        
        html_content += "</tbody></table>"    
    else:
        print("Problem in Connection...")
    # Close the cursor and connection
    cursor.close()
    cnxn.close()
    return render_template("base2.html",html_content=html_content)
    #return Response(html_content, mimetype='text/html')

@app.route("/base")
def renderBase():
    return render_template("base.html")

@app.route("/render")
def renderTemplate():
    return render_template("table-export.html", now=datetime.utcnow())


@app.route("/dashboard")
def renderDashboard():
    return render_template("index.html", now=datetime.utcnow())
    

@app.route("/base")
def renderBase():
    return render_template("base.html")
    

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        data = request.get_json()
        
        user_input = data.get('user_input', '')
        
        library = ["Abel","Abraham","Achille","Adel","Ademar","Adhemar","Adolf","Adrien","Agénor","Aimé","Alain","Albert","Albertet","Alexandre","Alexis","Alfred","Allain","Alphonse","Alphonse Joseph","Alvin","Amable","Amédée","Anatole","André","André-Marie","Ange","Anicet","Antoine","Anton","Antonin","Armand","Arnaud","Arnaut","Arsène","Arthur","Aubin","Auguste","Augustin","Aurèle","Aurélien","Aymard","Aymeric","Balthazar","Baptiste","Barthélemy","Bastien","Baudouin","Benjamin","Benoît","Bernard","Bertrand","Blanchard","Bruno","Calixte","Calvin","Camille","Camille Alphonse","Candide","Carolus","Cédric","Celestin","Cesar","Charle","Charles","Charles-Édouard","Charlot","Christian","Christophe","Claude","Claude-Henri","Clement","Clovis","Constant","Cyrille","Damien","Daniel","Danton","David","Delbert","Denis","Désiré","Didier","Dieudonné","Dominique","Donatien","Edgar","Edgard","Edmé","Edmond","Édouard","Élie","Élisée","Émile","Émilien","Emmanuel","Éric","Ernest","Erwan","Étienne","Fabien","Fabrice","Félicien","Felix","Ferdinand","Fernand","Flavien","Fleury","Florent","Florian","Florimond","Francis","Franck","François","François-Marie","François-Xavier","Frank","Frédéric","Fulbert","Fulgence","Gabriel","Gaël","Gaillard","Gaspard","Gaston","Gédéon","Geoffrey","Georges","Gérald","Gérard","Gerbaud","Germain","Ghislain","Gilbert","Gilles","Godfrey","Grégoire","Guillaume","Guy","Hadrien","Harold","Hector","Henri","Herbert","Hervé","Hilaire","Hippolyte","Honoré","Horace","Hubert","Hugo","Hugues","Hyacinthe","Ignace","Isidore","Ivo","Jacquelin","Jacques","Jacques-Désiré","Jacques-Marie","Jacquet","James","Jean","Jean-André","Jean-Antoine","Jean-Baptiste","Jean-Baptiste-Alphonse","Jean-Bernard","Jean-Charles","Jean-Christophe","Jean-Claude","Jean-Denis","Jean-Emmanuel","Jean-Étienne","Jean-François","Jean-Guy","Jean-Henri","Jean-Jacques","Jean-Joseph","Jean-Julien","Jean-Louis","Jean-Luc","Jean-Marc","Jean-Marie","Jean-Martin","Jean-Michel","Jean-Nicolas","Jean-Noël","Jean-Pascal","Jean-Paul","Jean-Philippe","Jean-Pierre","Jean-René","Jean-Robert","Jean-Sébastien","Jean-Yves","Jérémie","Jérémy","Jerome","Joël","Jonathan","Jules","Julien","Julien-Joseph","Just","Justin","Lauren","Laurence","Laurent","Lazare","Léandre","Léo","Leon","Léon","Loïc","Lothaire","Louis","Louis-Alphonse","Louis-Étienne","Loup","Luc","Lucas","Lucien","Ludo","Ludovic","Mainard","Manuel","Marc","Marc-André","Marcel","Marcellin","Marco","Mario","Martin","Mathieu","Matthias","Matthieu","Maurice","Maurille","Maxence","Maxime","Maximilien","Maynard","Medard","Melvin","Michel","Michel-Ange","Mikaël","Moise","Napoleon","Nicodème","Nicolas","Noe","Noel","Norbert","Odilon","Olivier","Pacôme","Pascal","Patrice","Patrick","Paul","Paul-Antoine","Paul-Louis","Paul-Marie","Philibert","Philippe","Phillippe","Pierre","Pierre-Édouard","Pierre-Julien","Pierre-Marie","Pierre-Paul","Pierre-Simon","Pierre-Yves","Pierrick","Profiat","Prosper","Quentin","Raimond","Rainier","Raoul","Raphael","Raymond","Réal","Réjean","Rémy","René","Reynald","Robert","Roger","Roland","Romain","Roman","Roméo","Romuald","Salome","Samuel","Sébastien","Ségolène","Seraphin","Servais","Severin","Simon","Stéphane","Stéphen","Sylvain","Sylvestre","Tancrède","Théodore","Théodule","Thibaut","Thierry","Thomas","Timothée","Titouan","Toussaint","Ulysse","Valentin","Vianney","Victor","Vincent","Virgile","Xavier","Yacine","Yann","Yannick","Yvan","Yves","Yvon","Zacharie"]

        # Get a list of suggestions with their scores
        suggestions_with_scores = process.extract(user_input, library, limit=5)

        # Filter out suggestions with a score below a certain threshold (e.g., 70)
        filtered_suggestions = [suggestion for suggestion, score in suggestions_with_scores if score >= 70]

        return jsonify({'suggestions': filtered_suggestions})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=8000)
