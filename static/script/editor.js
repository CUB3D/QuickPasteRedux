function computeLinecount() {
    let originalText = document.getElementById("editor-pane").value;

    let numbers = document.getElementById("numbers-list");
    // Remove all the numbers
    while(numbers.hasChildNodes()) {
        numbers.removeChild(numbers.lastChild);
    }

    // Add the numbers back
    for(let i = 0; i < originalText.split("\n").length; i++) {
        let elem = document.createElement("li");
        elem.textContent = "" + (i+1);

        numbers.appendChild(elem)
    }
}

document.onload = () => {
    computeLinecount();
};

function doSave(originalText) {
    let text = encodeURIComponent(originalText);

    if(text[text.length-1] === '\n')
        text = text.slice(0,-1);

    let r = new XMLHttpRequest();
    r.onload = () => {
        console.log("Got resp: " + r.status + ", " + r.responseText);
        document.getElementById("save-icon").style.visibility = "hidden";
    };

    const urlParts = window.location.href.split("/");
    const noteID = urlParts[urlParts.length-1];

    r.open("POST", "/saveNote/" + noteID, true);
    r.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    r.send('{"content": "' + text + '"}')
}

document.getElementById("btn-share").onclick = (e) => {
    let alert = document.getElementById("msg-overlay");
    let shareURL = window.location.href.replace("/edit/", "/view/");
    navigator.clipboard.writeText(shareURL).then(() => {
        alert.style.transition = "none";
        alert.style.opacity = "1";
        alert.style.visibility = "visible";
        setTimeout(() => {
            alert.style.transition = "";
            alert.style.opacity = "0";
        }, 1000);
        alert.innerText = "Link copied";
    })
};

document.getElementById("btn-public").onclick = (e) => {
    let r = new XMLHttpRequest();
    const urlParts = window.location.href.split("/");
    const noteID = urlParts[urlParts.length-1];
    r.open("GET", "/note/" + noteID + "/set-public", true);
    r.send();
};

let cm = CodeMirror.fromTextArea(document.getElementById("editor-pane"), {
    theme: "dark",
    // scrollbarStyle: "null",
    lineNumbers: true,
    autofocus: true
});

cm.on("change", (cm, change) => {
    doSave(cm.getValue());
});
