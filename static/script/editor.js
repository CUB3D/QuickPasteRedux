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