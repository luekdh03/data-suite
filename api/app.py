from flask import Flask, render_template, request, jsonify
import io 
import pandas as pd
import algo_las as algo_las

app = Flask(__name__)


## rendre le nombre des qcm de la séance las à l'interface web pour avoir le choix des reponses
@app.route('/upload-reponses-las-count-qcm', methods=['POST'])
def count_number_qcm_colle_las():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
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

@app.route('/upload-reponses-las-calcul-note', methods=['POST'])
def return_las_correction():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    if "shs" not in request.form or "answerlist" not in request.form:
        return jsonify({"error": "not all required fields provided"}), 400

    file = request.files['file']
    shs = True if request.form["shs"] == "true" else False
    correct_answers = request.form["answerlist"]

    try:
        # extraire les donnés du doc envoyé par iostream
        filedata = file.stream.read()
        filestream = io.StringIO(filedata.decode("UTF8"), newline=None)
        data = pd.read_csv(filestream)
        filestream.close()
        file.close()

        print(correct_answers.split(","))

        output_filename = algo_las.calculate_grade(data, correct_answers.split(","), shs)


    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({"filename": f"/static/outputLAS/{output_filename}"})
        

## Aspect visuel 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/correctionlas')
def correctionlas():
    return render_template('correctionlas.html')

if __name__ == '__main__':
    app.run()
