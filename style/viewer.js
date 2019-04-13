document.getElementById("btn-copy").onclick = function(e) {
    let content = document.getElementById("editor-pane").innerText.trim();
    navigator.clipboard.writeText(content);
};