function doSave() {
    let text = encodeURIComponent(document.getElementById("editor-pane").value);

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

document.getElementById("editor-pane").onkeydown = function(evt) {
    document.getElementById("save-icon").style.visibility = "visible";
    if(evt.ctrlKey && evt.key === "s") {
        doSave();
        evt.preventDefault();
    }
    doSave();
};