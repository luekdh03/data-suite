
QCM_NAME = "[[QCM_NAME]]"

REP_ENONCE = "[[ENONCE]]"

REP_ITEM_A = "[[ITEM-A]]"
REP_CORR_A = "[[CORR-A]]"
REP_FRAC_A = "[[FRACTION_A]]"

REP_ITEM_B = "[[ITEM-B]]"
REP_CORR_B = "[[CORR-B]]"
REP_FRAC_B = "[[FRACTION_B]]"

REP_ITEM_C = "[[ITEM-C]]"
REP_CORR_C = "[[CORR-C]]"
REP_FRAC_C = "[[FRACTION_C]]"

REP_ITEM_D = "[[ITEM-D]]"
REP_CORR_D = "[[CORR-D]]"
REP_FRAC_D = "[[FRACTION_D]]"

REP_ITEM_E = "[[ITEM-E]]"
REP_CORR_E = "[[CORR-E]]"
REP_FRAC_E = "[[FRACTION_E]]"

REP_ITEM_F = "[[ITEM-F]]"
REP_CORR_F = "[[CORR-F]]"
REP_FRAC_F = "[[FRACTION_F]]"

BEGIN_TXT = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>'
END_TXT = "</quiz>"


def get_question_xml_text(qcm):
    with open("api/static/format_type_question.xml", "r", encoding="utf-8") as f:
        format_type = f.read()

    format_type = format_type.replace(QCM_NAME, qcm.enonce[:8])  # shoud output 'QCM xx'

    format_type = format_type.replace(REP_ENONCE, qcm.enonce)
    
    format_type = format_type.replace(REP_ITEM_A, qcm.a)
    format_type = format_type.replace(REP_ITEM_B, qcm.b)
    format_type = format_type.replace(REP_ITEM_C, qcm.c)
    format_type = format_type.replace(REP_ITEM_D, qcm.d)
    format_type = format_type.replace(REP_ITEM_E, qcm.e)
    format_type = format_type.replace(REP_ITEM_F, qcm.f)

    format_type = format_type.replace(REP_CORR_A, qcm.a_correction)
    format_type = format_type.replace(REP_CORR_B, qcm.b_correction)
    format_type = format_type.replace(REP_CORR_C, qcm.c_correction)
    format_type = format_type.replace(REP_CORR_D, qcm.d_correction)
    format_type = format_type.replace(REP_CORR_E, qcm.e_correction)
    format_type = format_type.replace(REP_CORR_F, qcm.f_correction)

    if qcm.a_vrai:
        format_type = format_type.replace(REP_FRAC_A, "100")
    else:
        format_type = format_type.replace(REP_FRAC_A, "0")
    if qcm.b_vrai:
        format_type = format_type.replace(REP_FRAC_B, "100")
    else:
        format_type = format_type.replace(REP_FRAC_B, "0")
    if qcm.c_vrai:
        format_type = format_type.replace(REP_FRAC_C, "100")
    else:
        format_type = format_type.replace(REP_FRAC_C, "0")
    if qcm.d_vrai:
        format_type = format_type.replace(REP_FRAC_D, "100")
    else:
        format_type = format_type.replace(REP_FRAC_D, "0")
    if qcm.e_vrai:
        format_type = format_type.replace(REP_FRAC_E, "100")
    else:
        format_type = format_type.replace(REP_FRAC_E, "0")
    if qcm.f_vrai:
        format_type = format_type.replace(REP_FRAC_F, "100")
    else:
        format_type = format_type.replace(REP_FRAC_F, "0")

    return format_type

def get_xml(qcm_liste):
    final_text = "" + BEGIN_TXT

    for qcm in qcm_liste:
        final_text += "\n" + get_question_xml_text(qcm) + "\n"
    
    final_text += END_TXT

    return final_text



    





