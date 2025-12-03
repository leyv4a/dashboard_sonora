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
    fetch("/api/")
        .then(res => res.json())
        .then(data => {
            let valor = data["hermosillo_temperatura"];

            grafica.data.labels.push(new Date().toLocaleTimeString());
            grafica.data.datasets[0].data.push(valor);
            grafica.update();
        });
}

setInterval(actualizarDatos, 3000);
