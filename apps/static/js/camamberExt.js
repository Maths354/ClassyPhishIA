function initPieChart(url, nbURL) {
    console.log("d : ", url, nbURL)

    const ctx = document.getElementById('myPieChart');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: url,
            datasets: [{
                label: 'Extensions d\'URL',
                data: nbURL,
                backgroundColor: [  
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Diagramme camembert des extensions utilisé sur les sites de phishing.'
                }
            }
        }
    });
}

function initCertChart(cert, nbCert) {
    console.log("test : ", cert, nbCert)

    const ctx = document.getElementById('myCertChart');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: cert,
            datasets: [{
                label: 'Extensions d\'URL',
                data: nbCert,
                backgroundColor: [  
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Diagramme camembert des certificats utilisé sur les sites de phishing.'
                }
            }
        }
    });
}

