// charts.js - Manejo de gráficas dinámicas para dashboard
const charts = {};
const maxDataPoints = 20;
const dataHistory = {};
let historialCargado = false; // Flag para saber si ya cargamos el historial

// Configuración de colores por tipo
const typeColors = {
    temperatura: { bg: 'rgba(239, 68, 68, 0.2)', border: 'rgb(239, 68, 68)' },
    humedad: { bg: 'rgba(59, 130, 246, 0.2)', border: 'rgb(59, 130, 246)' },
    iluminacion: { bg: 'rgba(245, 158, 11, 0.2)', border: 'rgb(245, 158, 11)' },
    presion: { bg: 'rgba(139, 92, 246, 0.2)', border: 'rgb(139, 92, 246)' },
    viento: { bg: 'rgba(16, 185, 129, 0.2)', border: 'rgb(16, 185, 129)' },
    precipitacion: { bg: 'rgba(6, 182, 212, 0.2)', border: 'rgb(6, 182, 212)' },
    co2: { bg: 'rgba(220, 38, 38, 0.2)', border: 'rgb(220, 38, 38)' },
    ruido: { bg: 'rgba(234, 88, 12, 0.2)', border: 'rgb(234, 88, 12)' },
    default: { bg: 'rgba(102, 126, 234, 0.2)', border: 'rgb(102, 126, 234)' }
};

// Unidades por tipo
const typeUnits = {
    temperatura: '°C',
    humedad: '%',
    iluminacion: 'lux',
    presion: 'hPa',
    viento: 'km/h',
    precipitacion: 'mm',
    co2: 'ppm',
    ruido: 'dB'
};

/**
 * Crea una card HTML para un tipo de dato
 */
function createCard(tipo) {
    const colors = typeColors[tipo] || typeColors.default;
    const unit = typeUnits[tipo] || '';

    const card = document.createElement('div');
    card.className = `card ${tipo}`;
    card.id = `card-${tipo}`;
    card.innerHTML = `
        <div class="card-header">
            <h2 class="card-title">${tipo}</h2>
            <div>
                <span class="card-value" id="value-${tipo}">--</span>
                <span class="card-unit">${unit}</span>
            </div>
        </div>
        <div class="card-timestamp" id="timestamp-${tipo}">Esperando datos...</div>
        <div class="chart-container">
            <canvas id="chart-${tipo}"></canvas>
        </div>
    `;

    return card;
}

/**
 * Crea una gráfica de Chart.js
 */
function createChart(tipo) {
    const colors = typeColors[tipo] || typeColors.default;
    const unit = typeUnits[tipo] || '';
    const ctx = document.getElementById(`chart-${tipo}`);

    if (!ctx) {
        console.error(`Canvas no encontrado para ${tipo}`);
        return;
    }

    charts[tipo] = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: tipo.charAt(0).toUpperCase() + tipo.slice(1),
                data: [],
                borderColor: colors.border,
                backgroundColor: colors.bg,
                borderWidth: 2.5,
                tension: 0.4,
                fill: true,
                pointRadius: 3,
                pointHoverRadius: 6,
                pointBackgroundColor: colors.border,
                pointBorderColor: '#1e1e2e',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 750,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(30, 30, 46, 0.95)',
                    titleColor: '#f4f4f5',
                    bodyColor: '#e4e4e7',
                    borderColor: colors.border,
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    titleFont: {
                        size: 13,
                        weight: '600'
                    },
                    bodyFont: {
                        size: 12
                    },
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.y.toFixed(1)} ${unit}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#a1a1aa',
                        font: {
                            size: 11,
                            weight: '500'
                        },
                        callback: function(value) {
                            return value.toFixed(0) + ' ' + unit;
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#71717a',
                        font: {
                            size: 10
                        },
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });

    console.log(`✅ Gráfica creada para: ${tipo}`);
}

/**
 * Actualiza una card con nuevos datos
 */
function updateCard(tipo, valor, timestamp) {
    // Crear card si no existe
    if (!document.getElementById(`card-${tipo}`)) {
        console.log(`📊 Creando card para: ${tipo}`);
        const container = document.getElementById('cards-container');
        const card = createCard(tipo);
        container.appendChild(card);

        // Crear gráfica después de que el canvas esté en el DOM
        setTimeout(() => createChart(tipo), 100);

        // Inicializar historial
        dataHistory[tipo] = [];
    }

    // Actualizar valor actual
    const valueElement = document.getElementById(`value-${tipo}`);
    if (valueElement) {
        valueElement.style.transform = 'scale(1.1)';
        valueElement.textContent = valor.toFixed(1);
        setTimeout(() => {
            valueElement.style.transform = 'scale(1)';
        }, 200);
    }

    // Actualizar timestamp
    const timestampElement = document.getElementById(`timestamp-${tipo}`);
    if (timestampElement) {
        const date = new Date(timestamp);
        timestampElement.textContent = `Actualizado: ${date.toLocaleTimeString('es-MX')}`;
    }

    // Actualizar gráfica
    if (charts[tipo]) {
        const chart = charts[tipo];
        const time = new Date(timestamp).toLocaleTimeString('es-MX', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        // Agregar nuevo dato
        chart.data.labels.push(time);
        chart.data.datasets[0].data.push(valor);

        // Mantener solo los últimos maxDataPoints puntos
        if (chart.data.labels.length > maxDataPoints) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        // Actualizar gráfica
        chart.update('none');
    }

    // Ocultar mensaje de "no data"
    const noDataElement = document.getElementById('no-data');
    if (noDataElement) {
        noDataElement.style.display = 'none';
    }
}

/**
 * Carga el historial completo de un municipio
 */
function cargarHistorial(municipio) {
    console.log(`🔍 Cargando historial de: ${municipio}`);

    fetch(`/api/municipio/${municipio}/historial/`)
        .then(response => {
            console.log(`📡 Respuesta historial: ${response.status}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(historialCompleto => {
            console.log('📦 Historial recibido:', historialCompleto);

            // Verificar si hay datos
            if (Object.keys(historialCompleto).length === 0) {
                console.log('⚠️ No hay historial disponible');
                historialCargado = true;
                return;
            }

            // Procesar cada tipo de dato
            Object.entries(historialCompleto).forEach(([tipo, historial]) => {
                console.log(`📊 Procesando ${tipo}: ${historial.length} puntos`);

                // Crear la card si no existe
                if (!document.getElementById(`card-${tipo}`)) {
                    const container = document.getElementById('cards-container');
                    const card = createCard(tipo);
                    container.appendChild(card);
                }

                // Esperar a que el canvas esté listo
                setTimeout(() => {
                    // Crear gráfica si no existe
                    if (!charts[tipo]) {
                        createChart(tipo);
                    }

                    // Esperar a que la gráfica esté lista
                    setTimeout(() => {
                        if (charts[tipo] && historial.length > 0) {
                            const chart = charts[tipo];

                            // Limpiar datos existentes
                            chart.data.labels = [];
                            chart.data.datasets[0].data = [];

                            // Agregar todos los puntos del historial
                            historial.forEach(punto => {
                                const time = new Date(punto.timestamp).toLocaleTimeString('es-MX', {
                                    hour: '2-digit',
                                    minute: '2-digit',
                                    second: '2-digit'
                                });
                                chart.data.labels.push(time);
                                chart.data.datasets[0].data.push(punto.valor);
                            });

                            console.log(`✅ Gráfica de ${tipo} cargada con ${historial.length} puntos`);

                            // Actualizar card con el último valor
                            const ultimoPunto = historial[historial.length - 1];
                            const valueElement = document.getElementById(`value-${tipo}`);
                            if (valueElement) {
                                valueElement.textContent = ultimoPunto.valor.toFixed(1);
                            }

                            const timestampElement = document.getElementById(`timestamp-${tipo}`);
                            if (timestampElement) {
                                const date = new Date(ultimoPunto.timestamp);
                                timestampElement.textContent = `Actualizado: ${date.toLocaleTimeString('es-MX')}`;
                            }

                            // Actualizar gráfica
                            chart.update();
                        }
                    }, 200);
                }, 150);
            });

            // Ocultar mensaje de no data
            const noDataElement = document.getElementById('no-data');
            if (noDataElement) {
                noDataElement.style.display = 'none';
            }

            historialCargado = true;
            console.log('✅ Historial cargado completamente');
        })
        .catch(error => {
            console.log('ℹ️ No hay historial previo o error:', error.message);
            historialCargado = true;
        });
}

/**
 * Obtiene los datos actuales del servidor
 */
function fetchDatosActuales(municipio) {
    fetch(`/api/municipio/${municipio}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (Object.keys(data).length > 0) {
                // Actualizar cada tipo de dato
                Object.entries(data).forEach(([tipo, info]) => {
                    let valor, timestamp;

                    if (typeof info === 'object' && info.valor !== undefined) {
                        valor = info.valor;
                        timestamp = info.timestamp || new Date().toISOString();
                    } else {
                        valor = info;
                        timestamp = new Date().toISOString();
                    }

                    updateCard(tipo, valor, timestamp);
                });
            } else {
                // Mostrar mensaje solo si no se ha cargado historial
                if (!historialCargado) {
                    const noDataElement = document.getElementById('no-data');
                    if (noDataElement) {
                        noDataElement.style.display = 'block';
                    }
                }
            }
        })
        .catch(error => {
            console.error('❌ Error al obtener datos actuales:', error);
        });
}

/**
 * Inicializa el dashboard
 */
function initDashboard(municipio, updateInterval = 3000) {
    console.log(`🚀 Inicializando dashboard para: ${municipio}`);

    // 1. Cargar historial completo primero
    cargarHistorial(municipio);

    // 2. Después de 2 segundos, comenzar actualizaciones periódicas
    setTimeout(() => {
        console.log('🔄 Iniciando actualizaciones periódicas');
        fetchDatosActuales(municipio);
        setInterval(() => fetchDatosActuales(municipio), updateInterval);
    }, 2000);
}

// Exportar para uso en otros scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initDashboard, cargarHistorial, fetchDatosActuales, updateCard };
}