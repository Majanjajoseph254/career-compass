// Initialize chart instances
let skillsChart = null;
let industryChart = null;

// Update Skills Chart
function updateSkillsChart(skillsData) {
    const ctx = document.getElementById('skills-chart').getContext('2d');
    
    if (skillsChart) {
        skillsChart.destroy();
    }

    skillsChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: skillsData.map(skill => skill.name),
            datasets: [{
                label: 'Your Skills',
                data: skillsData.map(skill => skill.score),
                backgroundColor: 'rgba(74, 144, 226, 0.2)',
                borderColor: 'rgba(74, 144, 226, 1)',
                pointBackgroundColor: 'rgba(74, 144, 226, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(74, 144, 226, 1)'
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}

// Update Industry Chart
function updateIndustryChart(industryData) {
    const ctx = document.getElementById('industry-chart').getContext('2d');
    
    if (industryChart) {
        industryChart.destroy();
    }

    industryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: industryData.map(industry => industry.name),
            datasets: [{
                data: industryData.map(industry => industry.matchScore),
                backgroundColor: [
                    'rgba(74, 144, 226, 0.8)',
                    'rgba(39, 174, 96, 0.8)',
                    'rgba(241, 196, 15, 0.8)',
                    'rgba(231, 76, 60, 0.8)',
                    'rgba(155, 89, 182, 0.8)'
                ],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}% match`;
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });
}