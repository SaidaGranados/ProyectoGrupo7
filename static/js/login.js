
function mostrarClave() {
    var x = document.getElementById("clave");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
