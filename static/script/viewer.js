document.getElementById("btn-copy").onclick = function(e) {
    let alert = document.getElementById("msg-overlay");
    let content = document.getElementById("editor-pane").innerText.trim();
    navigator.clipboard.writeText(content).then(function () {
        alert.style.transition = "none";
        alert.style.opacity = "1";
        alert.style.visibility = "visible";
        setTimeout(function(){
            alert.style.transition = "";
            alert.style.opacity = "0";
        }, 1000);
        alert.innerText = "Note copied";
    });
};