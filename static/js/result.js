document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle (inherited from main script)
    
    // Animate progress circle
    const circle = document.querySelector('.progress-ring-circle-fill');
    if (circle) {
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (85 / 100) * circumference;
        
        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = circumference;
        
        setTimeout(() => {
            circle.style.strokeDashoffset = offset;
        }, 200);
    }
    
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const questionItems = document.querySelectorAll('.question-item');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const tabName = this.getAttribute('data-tab');
            
            // Show/hide questions based on tab
            questionItems.forEach(item => {
                if (tabName === 'all') {
                    item.style.display = 'block';
                } else if (item.classList.contains(tabName)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Initialize with incorrect questions shown
    if (tabButtons.length > 0) {
        tabButtons[0].click();
    }
    
    // Add animation to metric bars on scroll
    const animateMetricBars = function() {
        const metricBars = document.querySelectorAll('.metric-fill, .topic-fill');
        
        metricBars.forEach(bar => {
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
    
    window.addEventListener('scroll', animateMetricBars);
    animateMetricBars(); // Run once on page load
});