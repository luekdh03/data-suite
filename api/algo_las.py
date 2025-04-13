# Algorithme réalisé par Jasmine Truchot, ingénieure en data science
# Sœur de Solène Truchot, VP Data du tutorat, mandat 2023-2024
# Inspiré de l'algorithme écrit par Zakaria Belkacemi, Vp Site de la Fédération
# des Tutorats Santé de l'Université de Montpellier, Responsable Local de 
# tutoratsante.com et Vp Com au Tutorat Santé Nîmes. (Communication.tsn@gmail.com)
## Modifié par Luekar HERKE (VP DATA mandat 24/25) pour optimisation de la mise en 
# page sur GGSHEETS suite à la MAJ des tableurs et la mise en page conditionelle, et
# pour intégration dans la "DATASUITE"

n_info_cols = 3

def calculate_grade(answers_sheet, correct_answers, SHS):
    #print(correct_answers)
    answers_sheet = answers_sheet.fillna("")
    # Calculer le nombre de questions et d'étudiants
    n_qcm = (answers_sheet.shape[1] - n_info_cols)/6
    n_students = answers_sheet.shape[0]

    # Affiche un warning si le nombre de QMC calculé est non-entier
    if n_qcm != int(n_qcm):
        raise ValueError("Le nombre du QCM n'est pas int ! ") 
    
    #print(f"Nombre de QCMs : {int(n_qcm)}")
    #print(f"Nombre de candidats : {n_students}")
    
    # Créer un fichier texte pour y écrire les noms des candidats, les numéros
    # étudiants et les notes

    #FILENAME = "notes.txt"
    #FILEPATH = f'{os.path.join(os.getcwd(), "static", "outputLAS", FILENAME)}'
    #grades_file=open(FILEPATH,'w')
    grade_text = ""
    
    for k in range(1, n_students):
        student_grade = n_qcm
        student_line = answers_sheet.iloc[k].astype(str).to_list()
        grade_text += "\t".join(student_line[1:3]) + "\t"
        

        debug_text = f"student : {student_line[2]}, max grade : {n_qcm}, shs {SHS}\n"

        for i in range(int(n_qcm)):
            correct_qcm = correct_answers[6*i:6*(i+1)]
            student_qcm = student_line[3+6*i:3+6*(i+1)]

            debug_text += f"QCM{i+1} student: {student_qcm}, correct {correct_qcm}"

            #print(type(correct_qcm), student_qcm)
            #print(student_grade)

            # Gestion des F
            if correct_qcm[-1].lower() == "vrai":
                    if correct_qcm != student_qcm:
                            student_grade -= 1
                            #print("F faux")
            else:
                # Si quelqu'un a mis un F alors qu'il n'y en a pas
                if student_qcm[-1].lower() == "vrai":
                    student_grade -= 1
                    #print("F faux")
                    
                # Sinon, compter le nombre de réponses fausses
                else:
                    n_err = 0
                    for q in range(5):
                        if student_qcm[q].lower() != correct_qcm[q].lower():
                            n_err += 1
                    #print(f"Err : {n_err}")
                    
                    # Barème classique
                    if not SHS:
                        if n_err == 1:
                            student_grade -= 0.25
                        elif n_err == 2:
                            student_grade -= 0.5
                        elif n_err >= 3:
                            student_grade -= 1
                    
                    # Barème de SHS
                    else:
                        if n_err == 1:
                            student_grade -= 0.5
                        elif n_err >= 2:
                            student_grade -= 1
            
            debug_text += f" new grade : {student_grade}\n"
        #raise ValueError(debug_text)
            

                        
        grade_text += str(student_grade).replace(".", ",") +"\n"
        #print(f"{student_line[1]}, {student_line[2]} : {student_grade}")
        
    return grade_text
