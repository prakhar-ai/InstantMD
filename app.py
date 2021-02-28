from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import re
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PatientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(5))
    story = db.Column(db.String(2000))
    complaint = db.Column(db.String(300))
    symptoms = db.Column(db.String(200))
    duration = db.Column(db.String(200))
    severity = db.Column(db.String(200))
    asymptom = db.Column(db.String(200))
    afactors = db.Column(db.String(300))
    rfactors = db.Column(db.String(300))


@app.route("/")
@app.route("/home")		
def home():
    return render_template('home.html', active='home')


@app.route("/evaluate")		
def evaluate():
    return render_template('evaluate.html', title='Evaluation', active='evaluate')

@app.route("/database")		
def database():
    Patientlist = PatientData.query.all()
    return render_template('database.html', title='Database', active='database',Patientlist=Patientlist)

@app.route("/statistics")			
def statistics():
    return render_template('statistics.html', title='Statistics', active='statistics')


@app.route("/howitworks")	
def howitworks():
    return render_template('howitworks.html', title='How it works', active='howitworks')


@app.route("/credits")		
def credits():
    return render_template('creditspage.html', title='Credits', active='credits')

@app.route("/add", methods=["POST"])
def add():
    story = request.form.get("story")
    gender  = request.form.get("gender")
    name  = request.form.get("fullname")
    complaint = request.form.get("complaint")
    symptoms  = request.form.get("symptoms")
    duration  = request.form.get("duration")
    severity  = request.form.get("severity")
    asymptom  = request.form.get("asymptom")
    rfactor  = request.form.get("rfactor")
    afactor  = request.form.get("afactor")
    new_data = PatientData(story=story, name=name, gender=gender, complaint=complaint,symptoms=symptoms,duration=duration,severity=severity,asymptom=asymptom,rfactors=rfactor,afactors=afactor)
    db.session.add(new_data)
    db.session.commit()
    return redirect(url_for("database"))

@app.route("/report", methods=["POST"])
def report():
    story = request.form.get("story")
    gender  = request.form.get("gender")
    name  = request.form.get("fullname")
    # need to integrate InstaMD function from classification.ipynb here
    # This route is called from "evaluate.html" and renders "report.html" with results
    def InstantMD(story,gender,name):
        symptom_list =  []
        with open('symptom_list.txt', 'r') as filehandle:
            for line in filehandle:
                symptom = line[:-1]
                symptom_list.append(symptom)
        anatomy_list =  []
        with open('anatomy_list.txt', 'r') as filehandle:
            for line in filehandle:
                anatomy = line[:-1]
                anatomy_list.append(anatomy)

        Symptoms = {}
        Anatomy = {}

        story = story.replace(',', '.').replace('?', '.')
        sentences = story.split('.')

        word_list = []
        for i in sentences:
            words = i.split(" ")
            word_list = word_list + words

        while("" in word_list) : 
            word_list.remove("") 


        for i in symptom_list:
            if((' ' in i) == True):
                if story.count(i)>0:
                    Symptoms[i] = story.count(i)

        for i in symptom_list:
            if word_list.count(i)>0:
                Symptoms[i] = word_list.count(i)

        for i in anatomy_list:
            if word_list.count(i)>0:
                Anatomy [i] = word_list.count(i)

        number_dict = {"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}
        for i in range(len(word_list)):
            if word_list[i] in list(number_dict.keys()):
                word_list[i] = number_dict[word_list[i]]

        chief_complaint_final = ""
        duration_final = ""
        aggravating_factor_final = ""
        relieving_factor_final = ""
        associated_symptom_final= ""
        severity_final = ""
        symptoms_final = ""

        aggrevating_factor_keywords = ["increase","increases","increasing","rise","rises","becomes more",]
        relieving_factor_keywords = ["decreases", "decrease" , "decreasing" , "lessens" , "less" , "subsides", "subside","better"]

        duration_list_postfix = ["month","year","week","day","months","years","weeks","days"]


        for i in sentences:
            symptoms = set(Symptoms.keys())
            anatomy = set(Anatomy.keys())
            words = set(i.split(" "))
            if len(symptoms & words)!=0 and len(anatomy & words)!=0:
                chief_complaint_final = ' and '.join(list(symptoms & words)) + ",  area: " + " and ".join(list(anatomy & words))
                break

        if (chief_complaint_final == ""):
            chief_complaint_final = max(Symptoms, key=Symptoms.get) 

        symptoms_final = list(Symptoms.keys())

        for i in duration_list_postfix:
            if i in word_list:
                index = word_list.index(i) - 1
                duration_final = word_list[index] + " " + word_list[index + 1]
                break

        def get_aggravating_factor():
            for i in sentences:
                words = set(i.split(" "))
                for keyword in aggrevating_factor_keywords:
                    if keyword in words:
                        result = re.search(keyword + '(.*)and', i)
                        if(result == None):
                            result = re.search(keyword + '(.*)', i)
                        return keyword + result.group(1)


        def get_relieving_factor():
            for i in sentences:
                words = set(i.split(" "))
                for keyword in relieving_factor_keywords:
                    if keyword in words:
                        result = re.search(keyword + '(.*)', i)
                        return keyword + result.group(1)


        def get_associated_symptom():
            for i in sentences:
                words = set(i.split(" "))
                keyword = "also"
                if keyword in words:
                    result = re.search(keyword + '(.*)', i)
                    return  result.group(1)

        def get_severity():
            if "mild" in word_list:
                return "mild"
            elif "moderate" in word_list:
                return  "moderate"
            elif "severe" in word_list:
                return  "severe"
            elif story.count("pain")>1:
                return  "severe"
            elif story.count("pain")==1:
                return  "severe"
            else:
                return  "mild"

        aggravating_factor_final = get_aggravating_factor()
        relieving_factor_final = get_relieving_factor()
        associated_symptom_final= get_associated_symptom()
        severity_final = get_severity()
        
        report_dict = {
            "Symptoms" : symptoms_final,
            "Chief Complaint": chief_complaint_final,
            "Duration" : duration_final,
            "Aggravating Factor" : aggravating_factor_final,
            "Relieving Factor" : relieving_factor_final,
            "Associated Symptom" : associated_symptom_final,
            "Severity": severity_final,
            "Story" : story,
            "Gender" : gender,
            "Name" : name    
        }
        return report_dict


    report_dict = InstantMD(story,gender,name)
    return render_template('report.html', title='Report', active='report',report_dict=report_dict)
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)		
