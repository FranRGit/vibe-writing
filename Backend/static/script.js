async function enviar() {
    const texto = document.getElementById("textarea").value;
    const res = await fetch("/api/responder", {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({texto:texto})
    })

    const data = await res.json()
    document.getElementById("respuesta").textContent = data.respuesta;
}

document.getElementById("modelo").addEventListener("change", function () {
    const modeloSeleccionado = this.value;

    fetch("/api/set_model", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ modelo: modeloSeleccionado }),
    }).then(res => res.json())
    .then(data => {
        console.log("Modelo actualizado:", data.modelo);
        document.getElementById("modelo-actual").textContent = data.modelo;

    });
});