import fitz

class QCM:
    def __init__(self):
        self.qcm = ""
        self.enonce = ""
        self.a = ""
        self.b = ""
        self.c = ""
        self.d = ""
        self.e = ""
        self.f = ""

        self.images = []

        self._stream_index = "" # A, B, C, D, E, F

    def _eval_begin(self, letter, line):
        if line[:3] == f"{letter}. " or (len(line) <= 2 and line[:2] == f"{letter}."):
            self._stream_index = letter

    def stream(self, line):
        # Si le premiere lettre est ABCDEF + ". " on a un nouveau item -> mettre le index  
        for letter in list("ABCDEF"):
            self._eval_begin(letter, line)
        
        # en fonction de index ajouter à l'item
        if self._stream_index == "A":
            self.a += line
        elif self._stream_index == "B":
            self.b += line
        elif self._stream_index == "C":
            self.c += line
        elif self._stream_index == "D":
            self.d += line
        elif self._stream_index == "E":
            self.e += line
        elif self._stream_index == "F":
            self.f += line
        else: # cela evite de mettre un moreau ou il appartient pas
            try: enc = ord(line[0]), ord(line[1]), ord(line[2])
            except IndexError: enc = "Out of range"
            raise ValueError(f"_stream_index has to be A,B,C,D,E,F and not '{self._stream_index}'\n+Concerning line '{line}' in '{self.qcm}' \n + encoding ascii of the first the letters : {enc} \n\n {self}")
    
    def stream_image(self, img):
        if self.f:
            self.images.append(("F", img))
        elif self.e:
            self.images.append(("E", img))
        elif self.d:
            self.images.append(("D", img))
        elif self.c:
            self.images.append(("C", img))
        elif self.b:
            self.images.append(("B", img))
        elif self.a :
            self.images.append(("A", img))
        elif self.enonce:
            self.images.append(("Enonce", img))
        else:
            self.images.append((None, img))

    def __str__(self):
        return f'{self.qcm}{self.enonce}\n{self.a}\n{self.b}\n{self.c}\n{self.d}\n{self.e}\n{self.f}'


class QCM_CORR:
    def __init__(self, enonce, correct) -> None:
        self.qcm_enonce = enonce
        self.qcm_correct = correct

        self.correct_list = []

        self.enonce = enonce.enonce
        self.enonce_corr = correct.enonce

        self.images = enonce.images
        self.images_corr = correct.images

        self.a = enonce.a
        self.a_correction = correct.a
        self.a_vrai = self.is_vrai(correct.a)
        if self.a_vrai:
            self.correct_list.append("A")

        self.b = enonce.b
        self.b_correction = correct.b
        self.b_vrai = self.is_vrai(correct.b)
        if self.b_vrai:
            self.correct_list.append("B")

        self.c = enonce.c
        self.c_correction = correct.c
        self.c_vrai = self.is_vrai(correct.c)
        if self.c_vrai:
            self.correct_list.append("C")

        self.d = enonce.d
        self.d_correction = correct.d
        self.d_vrai = self.is_vrai(correct.d)
        if self.d_vrai:
            self.correct_list.append("D")

        self.e = enonce.e
        self.e_correction = correct.e
        self.e_vrai = self.is_vrai(correct.e)
        if self.e_vrai:
            self.correct_list.append("E")

        self.f = enonce.f
        self.f_correction = correct.f
        self.f_vrai = self.is_vrai(correct.f)
        if self.f_vrai:
            self.correct_list.append("F")

    def is_vrai(self, corr):
        if corr[3:7] == "Vrai" or corr[2:6] == "Vrai":
            return True
        if corr[3:7] == "Faux" or corr[2:6] == "Faux":
            return False
        print(f"Error !!! {corr[3:8]} n'est pas vrai ou faux, {corr}")
        return None


def get_qcms(filestream):
    pdf = fitz.open(stream=filestream, filetype="pdf")

    qcms = []
    qcm_stream = False
    current_qcm = None

    for page in pdf:
        blocks = page.get_text("dict")["blocks"] 
        sorted_blocks = sorted(blocks, key=lambda x: x["bbox"][1])
        for block in sorted_blocks:
            if block["type"] == 0: ## STR
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"])
                        txt = span["text"]
                        if size == 14.0 or size == 12.0: ## enoncé
                            if not qcm_stream: ## si la ligne avant était pas un enoncé
                                if txt[:3] == "QCM": # commencer un nouveau qcm
                                    if current_qcm: qcms.append(current_qcm) # si il avait un qcm avant - enregistrer
                                    current_qcm = QCM()
                                    qcm_stream = True
                            if current_qcm : current_qcm.enonce += txt
                        elif size == 11.0: ## item
                            if current_qcm: # si on est dans un qcm
                                try: # cela evite des characteres random de perturber le stream
                                    current_qcm.stream(txt)
                                    qcm_stream=False # si on detecte un debut de qcm il faut arreter l'enoncé
                                except ValueError as e: 
                                    print(e)
            elif block["type"] == 1: ## IMG
                if current_qcm: 
                    image = block["image"]
                    current_qcm.stream_image(image)

    qcms.append(current_qcm)
    return qcms


def fuse_qcms(enonces, corrs):
    if len(enonces) != len(corrs):
        raise ValueError("len enonces != len corrections")
    fuse = []
    for i in range(len(enonces)):
        fuse.append(QCM_CORR(enonces[i], corrs[i]))
    return fuse

if __name__ == "__main__":
    print(get_qcms("ex.pdf"))
