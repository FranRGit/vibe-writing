async function enviar() {
    const texto = document.getElementById("textarea").value;
    const res = await fetch("/api/responder", {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({prompt:texto})
    })

    const data = await res.json()
    document.getElementById("respuesta").textContent = data.respuesta;
}