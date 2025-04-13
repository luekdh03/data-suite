from flask import Flask, render_template, request, jsonify

import api.loadpdf as loadpdf
import api.to_xml_moodle as to_xml_moodle
import api.algo_las as algo_las

from datetime import datetime
import pandas as pd
import io

app = Flask(__name__)


## Gilles LAS
@app.route("/correctionlas")
def grilleLAS():
    return render_template("grillelas.html")

@app.route("/las-count-qcm", methods=["POST"])
def lascountqcm():
    file = request.files.get("reponses")
    if not file:
        return jsonify({"error": "Pas de fichier donnée"}), 500
    try:
        # extraire les donnés du doc envoyé par iostream
        filedata = file.stream.read()
        filestream = io.StringIO(filedata.decode("UTF8"), newline=None)
        data = pd.read_csv(filestream)
        
        # compter nombres QCM
        n_qcm = (data.shape[1] - algo_las.n_info_cols)/6

        filestream.close()
        file.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'rows': n_qcm})

@app.route("/las-calc-note", methods=["POST"])
def lascalcnotes():
    try: 
        file = request.files.get("reponses")
        shs = True if request.form.get("shs") else False
        answers = request.form.get("answerlist").split(",")
    except Exception as e:
        return jsonify({"error": f"Non possible de lire POST : {e}"}), 500

    try:
        # extraire les donnés du doc envoyé par iostream
        filedata = file.stream.read()
        filestream = io.StringIO(filedata.decode("UTF8"), newline=None)
        data = pd.read_csv(filestream)
    except Exception as e :
        return jsonify({"error": f"Non possible de passer en filestream : {e}"}), 500
    
    try:
        output = algo_las.calculate_grade(data, answers, shs)
    except Exception as e:
        return jsonify({"error": f"Non possible de générer output : {e}"}), 500

    return jsonify({"output": output})
    




## AUTO QCM
@app.route("/autoqcm")
def autoQCM():
    return render_template("autoqcm.html")


@app.route("/uploadAutoQCM", methods=["POST"])
def uploadAutoQCM():
    enonce = request.files.get("enonce")
    corr = request.files.get("correction")

    if not enonce or not corr:
        return jsonify({"message": f"Donnez les deux documents ! \n {type(enonce), type(corr)}"}), 400
    
    enonce_bytes = enonce.stream.read()
    corr_bytes = corr.stream.read()

    try: 
        qcms_enonce = loadpdf.get_qcms(enonce_bytes)
        qcms_corr = loadpdf.get_qcms(corr_bytes)
    except Exception as e:
        return jsonify({"message": f"Erreur pendant lecture des PDF : {e}"}), 500

    try:
        qcm = loadpdf.fuse_qcms(qcms_enonce, qcms_corr)
    except ValueError as e:
        return jsonify({"message": f"Pas possible de fusionner : {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"Erreur pendant fusion PDF : {e}"}), 500
    
    try:
        xml = to_xml_moodle.get_xml(qcm)
    except Exception as e:
        return jsonify({"message": f"Erreur pendant création XML : {e}"}), 500

    
    enonces_text = [i.enonce for i in qcm]

    now = datetime.now()
    filename = f"xmlmoodle_{now:%d-%m-%Y_%Hh%Mmin%Ss}"

    try:
        return jsonify({"xml": xml, "qcms":enonces_text, "filename": filename}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur pendant return : {e}"}), 500




@app.route("/")
def homescreen():
    return render_template("index.html")