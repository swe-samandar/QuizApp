document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle (inherited from main script)
    
    // User menu toggle
    const userMenu = document.querySelector('.user-menu');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    userMenu.addEventListener('click', function(e) {
        // Prevent closing when clicking inside dropdown
        if (e.target.closest('.dropdown-menu')) return;
        
        const isOpen = dropdownMenu.style.opacity === '1' || 
                      dropdownMenu.classList.contains('open');
        
        if (isOpen) {
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.transform = 'translateY(-10px)';
            dropdownMenu.classList.remove('open');
        } else {
            dropdownMenu.style.opacity = '1';
            dropdownMenu.style.visibility = 'visible';
            dropdownMenu.style.transform = 'translateY(0)';
            dropdownMenu.classList.add('open');
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!userMenu.contains(e.target)) {
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.transform = 'translateY(-10px)';
            dropdownMenu.classList.remove('open');
        }
    });
    
    // Animate progress bars on scroll
    const animateProgressBars = function() {
        const progressSection = document.querySelector('.progress-section');
        if (!progressSection) return;
        
        const sectionPosition = progressSection.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (sectionPosition < screenPosition) {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
            
            // Remove event listener after animation
            window.removeEventListener('scroll', animateProgressBars);
        }
    };
    
    window.addEventListener('scroll', animateProgressBars);
    animateProgressBars(); // Run once on page load
    
    // Add hover effects to recommended tests
    const recommendedItems = document.querySelectorAll('.recommended-item');
    recommendedItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.recommended-icon');
            icon.style.transform = 'scale(1.1)';
            icon.style.color = 'var(--primary-light)';
        });
        
        item.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.recommended-icon');
            icon.style.transform = 'scale(1)';
            icon.style.color = 'var(--primary-color)';
        });
    });
});