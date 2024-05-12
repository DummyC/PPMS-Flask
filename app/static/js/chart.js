var ctx = document.getElementById('doughnut').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Approved', 'Pending', 'Rejected'],
        datasets: [{
            label: 'Project Summary',
            data: [${approved}, ${pending}, ${rejected}],
            backgroundColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 0, 0, 1)',
            ],
            borderColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 0, 0, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: false,
        plugins: {
            legend: {
              display: true,
              position: 'right'
            }
          }
    }
});