document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle (inherited from main script)
    
    // Initialize Activity Chart
    const ctx = document.getElementById('activityChart').getContext('2d');
    const activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Tests Taken',
                data: [12, 19, 15, 22, 18, 25, 28],
                borderColor: 'rgba(108, 92, 231, 1)',
                backgroundColor: 'rgba(108, 92, 231, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }, {
                label: 'Average Score',
                data: [75, 82, 78, 85, 88, 86, 89],
                borderColor: 'rgba(0, 206, 201, 1)',
                backgroundColor: 'rgba(0, 206, 201, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    // Update chart based on time filter
    const timeFilter = document.querySelector('.time-filter');
    timeFilter.addEventListener('change', function() {
        // In a real app, this would fetch new data based on the filter
        // For demo purposes, we'll just animate the chart
        activityChart.data.datasets.forEach(dataset => {
            dataset.data = dataset.data.map(value => value + (Math.random() * 10 - 5));
        });
        activityChart.update();
    });
    
    // Animate skill bars on scroll
    const animateSkillBars = function() {
        const skillBars = document.querySelectorAll('.skill-level');
        
        skillBars.forEach(bar => {
            const rect = bar.parentElement.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
            
            if (isVisible && !bar.classList.contains('animated')) {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                    bar.classList.add('animated');
                }, 100);
            }
        });
    };
    
    window.addEventListener('scroll', animateSkillBars);
    animateSkillBars(); // Run once on page load
    
    // Add responsive labels to table cells
    function setupResponsiveTable() {
        if (window.innerWidth < 768) {
            const headers = document.querySelectorAll('.table-header .table-cell');
            const rows = document.querySelectorAll('.table-row');
            
            // Get header labels
            const labels = [];
            headers.forEach(header => {
                labels.push(header.textContent);
            });
            
            // Add data-label attributes
            rows.forEach(row => {
                const cells = row.querySelectorAll('.table-cell');
                cells.forEach((cell, index) => {
                    cell.setAttribute('data-label', labels[index]);
                });
            });
        }
    }
    
    // Run on load and resize
    setupResponsiveTable();
    window.addEventListener('resize', setupResponsiveTable);
    
    // Avatar edit functionality
    const avatarEdit = document.querySelector('.avatar-edit');
    if (avatarEdit) {
        avatarEdit.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Avatar upload functionality would be implemented here!');
            // In a real app, this would open a file upload dialog
        });
    }
});