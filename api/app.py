from flask import Flask, render_template, request, send_file, jsonify
import api.loadpdf as loadpdf
import api.to_xml_moodle as to_xml_moodle
from datetime import datetime

app = Flask(__name__)


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

@app.route("/autoqcm")
def autoQCM():
    return render_template("autoqcm.html")


@app.route("/")
def homescreen():
    return render_template("index.html")