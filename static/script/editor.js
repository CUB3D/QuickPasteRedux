function computeLinecount() {
    let originalText = document.getElementById("editor-pane").value;

    let numbers = document.getElementById("numbers-list");
    // Remove all the numbers
    while(numbers.hasChildNodes()) {
        numbers.removeChild(numbers.lastChild);
    }

    // Add the numbers back
    for(var i = 0; i < originalText.split("\n").length; i++) {
        let elem = document.createElement("li");
        elem.textContent = "" + (i+1);


        numbers.appendChild(elem)
        //
        // let lastNode = numbers.lastChild;
        //
        // if(lastNode != null) {
        //     lastNode = lastNode.nextSibling;
        // }
        //
        // numbers.insertBefore(elem, lastNode);
    }
}

document.onload = function() {
    computeLinecount();
};

function doSave() {
    let originalText = document.getElementById("editor-pane").value;
    let text = encodeURIComponent(originalText);

    if(text[text.length-1] === '\n')
        text = text.slice(0,-1);

    let r = new XMLHttpRequest();
    r.onload = function() {
        console.log("Got resp: " + r.status + ", " + r.responseText);
        document.getElementById("save-icon").style.visibility = "hidden";
    };

    const urlParts = window.location.href.split("/");
    const noteID = urlParts[urlParts.length-1];

    r.open("POST", "/saveNote/" + noteID, true);
    r.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    r.send('{"content": "' + text + '"}')
}

let editorPane = document.getElementById("editor-pane");
editorPane.onkeydown = function(evt) {
    document.getElementById("save-icon").style.visibility = "visible";
    if(evt.ctrlKey && evt.key === "s") {
        doSave();
        evt.preventDefault();
    }
    computeLinecount();
    doSave();
};
// editorPane.onkeyup = function() {
//     computeLinecount();
// };

document.getElementById("btn-share").onclick = function(e) {
    let alert = document.getElementById("msg-overlay");
    let shareURL = window.location.href.replace("/edit/", "/view/");
    navigator.clipboard.writeText(shareURL).then(function () {
        alert.style.transition = "none";
        alert.style.opacity = "1";
        alert.style.visibility = "visible";
        setTimeout(function(){
            alert.style.transition = "";
            alert.style.opacity = "0";
        }, 1000);
        alert.innerText = "Link copied";
    })
};