function doSave() {
    let text = document.getElementById("edit-pane").innerText;
    console.log("Text: " + text);
    console.log("TXT: " + encodeURIComponent(text));
}

document.onkeydown = function(evt) {
    if(evt.ctrlKey && evt.key === "s") {
        doSave();
        evt.preventDefault();
    }
};