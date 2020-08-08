document.getElementById("btn-copy").onclick = (e) => {
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

document.getElementById("btn-clone").onclick = (e) => {
    let r = new XMLHttpRequest();
    r.onload = () => {
        document.location.href = "/edit/" + r.responseText;
    };

    const urlParts = window.location.href.split("/");
    const noteID = urlParts[urlParts.length-1];

    r.open("POST", "/clone/" + noteID, true);
    r.send();
};

ukauth.init({
    APP_ID: "3qiADDS0c3ik0MAvgYuYno25PstbBl9o"
});
ukauth.onLogin((user) => {
    console.log(user.username + " has logged in");
});
ukauth.oneClickLogin();
