var rownumbers = 0;

// créer le handle pour le button pour telecharger les reponses
document.getElementById("uploadButton").addEventListener("click", async () => {
    const form = document.getElementById("fileForm");
    const uploadInput = document.getElementById("file-upload");
    const uploadButton = document.getElementById("uploadButton");
    const correctionButton = document.getElementById("correctionButton");
    const formData = new FormData(form);

    uploadInput.disabled = true;
    uploadButton.hidden = true;
    correctionButton.hidden = false;

    try {
        const response = await fetch('/upload-reponses-las-count-qcm', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error("File upload failed");
        }

        const { rows } = await response.json();
        generateRows(rows);
    } catch (error) {
        console.error("Error:", error);
    }
});

// handle du button pour telecharger les bonnes reponses.
document.getElementById("correctionButton").addEventListener("click", async () => {
    const form = document.getElementById("fileForm");
    const uploadInput = document.getElementById("file-upload");
    uploadInput.disabled = false;
    const formData = new FormData(form);
    uploadInput.disabled = true;

    // get awnser list
    var answerlist = [];
    for (let i = 1; i <= rownumbers; i++) {
        ["A", "B", "C", "D", "E", "F"].forEach((item) => {
            // if line checked
            if (document.getElementById(`QCM${i}${item}`).checked) answerlist.push("Vrai")
            else answerlist.push("")
        });
    }
    
    // submit to main program

    formData.append("answerlist", answerlist)
    formData.append("shs", "false")

    try {
        const response = await fetch('/upload-reponses-las-calcul-note', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error("File upload failed");
        }

        const { filename } = await response.json();
        downloadURI(filename, "output.txt")

    } catch (error) {
        console.error("Error:", error);
    }
});

// afficher le bon nombre des qcm
function generateRows(numberOfRows) {
    rownumbers = numberOfRows;

    const scrollContent = document.getElementById("scrollContent");
    
    console.debug(scrollContent)
    scrollContent.innerHTML = ""; 


    for (let i = 1; i <= numberOfRows; i++) {
        const row = document.createElement("div");
        row.className = "row";

        const label = document.createElement("span");
        label.textContent = `QCM ${i}`;
        row.appendChild(label);

        ["A", "B", "C", "D", "E", "F"].forEach((item) => {
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.id = `QCM${i}${item}`;

            const checkboxLabel = document.createElement("label");
            checkboxLabel.htmlFor = checkbox.id;
            checkboxLabel.textContent = item;

            row.appendChild(checkbox);
            row.appendChild(checkboxLabel);
        });

        scrollContent.appendChild(row);
    }
}

function downloadURI(uri, name) 
{
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    link.click();
}