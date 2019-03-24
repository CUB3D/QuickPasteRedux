function doSave() {
    let text = document.getElementById("edit-pane").innerText;
    console.log("Text: " + text);
    console.log("TXT: " + encodeURIComponent(text));

    let r = new XMLHttpRequest();
    r.onload = function() {
        console.log("Got resp: " + r.status + ", " + r.responseText);
    };
    r.open("POST", "/saveNote/asdf", true);
    r.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    r.send('{"content": "' + text + '"}')
}

document.onkeydown = function(evt) {
    if(evt.ctrlKey && evt.key === "s") {
        doSave();
        evt.preventDefault();
    }
};