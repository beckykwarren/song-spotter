# import necessary libraries
import flask as f
from flask_pymongo import PyMongo
import pymongo, os, json, pyperclip

#------------


# Create an instance of Flask
app = f.Flask(__name__)

# Database Setup
global list_of_users
global firstUser

# mongo = pymongo.MongoClient("mongodb://localhost:27017")
# db = mongo.spotify



client = pymongo.MongoClient("mongodb+srv://beckykwarren:Purple37&@songs-hpw2t.mongodb.net/test?retryWrites=true&w=majority")
db = client.spotify


list_of_users = db.list_collection_names() 
firstUser = list_of_users[0]

collection = db[firstUser]
# You're first user is {firstUser}.

print(f"""
--------------
Here is a list of collections in your MongoDB:
{list_of_users}
Your first user is {firstUser}.
You are connected to {collection.full_name}
-----------
""")
print(collection)

global username
global usertoken



# create route that renders index.html template
@app.route("/")
def home():
    list_of_users = db.list_collection_names()
    songs = collection.find() 
    return f.render_template("index.html", list_of_users = list_of_users,songs=songs)

@app.route("/swarm")
def swarm():
    songs = collection.find() 
    print(collection.full_name)   
    return f.render_template("swarm.html",songs=songs)

@app.route("/popularity")
def pop():
    songs = collection.find()    
    return f.render_template("barchart.html",songs=songs)

@app.route("/bubble")
def bubble():
    songs = collection.find()    
    return f.render_template("bubble.html",songs=songs)
    
@app.route("/cloud")
def cloud():
    songs = collection.find()    
    return f.render_template("wordcloud.html",songs=songs)

@app.route("/gotID", methods=["GET", "POST"])
def gotID():
    global username
    global collection
    if f.request.method == "POST":
        username = f.request.form["username"]
        print(f"Username: {username}")
        collection = db[username]
        return f.redirect("/popularity")
    return f.render_template("index.html")

@app.route("/gotToken", methods=["GET", "POST"])
def gotToken():
    global usertoken
    import spoti
    if f.request.method == "POST":
        usertoken = f.request.form["usertoken"]
        print(f"Token: {usertoken}")
        return f.redirect("/")

        # run the getting a token code??

    return f.render_template("form2.html")

@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    global usertoken
    return f.render_template("form.html")

@app.route("/getdata")
def get():
    print("running getdata route")

    documents = collection.find()

    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    
    return json.dumps(response)

@app.route("/getusers")
def getuserlist():
    print("running getusers route")
    
    return json.dumps(list_of_users)



if __name__ == "__main__":
    app.run(debug=True)
