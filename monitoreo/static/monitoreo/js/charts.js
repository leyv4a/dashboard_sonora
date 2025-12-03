const municipio = window.municipio; // viene desde dashboard.html

let ctx = document.getElementById("graficaTemperatura").getContext("2d");

let grafica = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Temperatura",
            data: [],
            borderWidth: 2
        }]
    }
});

function actualizarDatos() {
    fetch(`/api/datos/${municipio}/`)
        .then(res => res.json())
        .then(data => {

            let valor = data["temperatura"]; // ahora es por municipio

            if (valor !== undefined) {
                grafica.data.labels.push(new Date().toLocaleTimeString());
                grafica.data.datasets[0].data.push(valor);
                grafica.update();
            }
        });
}

setInterval(actualizarDatos, 2000);
