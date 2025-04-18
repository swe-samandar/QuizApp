document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle (inherited from main script)
    
    // View toggle functionality
    const viewButtons = document.querySelectorAll('.view-btn');
    const testView = document.getElementById('test-view');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            viewButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const viewType = this.getAttribute('data-view');
            testView.className = viewType === 'list' ? 'test-list-view' : 'test-grid';
        });
    });
    
    // Filter functionality
    const categoryFilter = document.getElementById('category-filter');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const testCards = document.querySelectorAll('.test-card');
    const categoryCards = document.querySelectorAll('.category-card');
    
    function filterTests() {
        const selectedCategory = categoryFilter.value;
        const selectedDifficulty = difficultyFilter.value;
        
        testCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            const cardDifficulty = card.getAttribute('data-difficulty');
            
            const categoryMatch = !selectedCategory || cardCategory === selectedCategory;
            const difficultyMatch = !selectedDifficulty || cardDifficulty === selectedDifficulty;
            
            if (categoryMatch && difficultyMatch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    categoryFilter.addEventListener('change', filterTests);
    difficultyFilter.addEventListener('change', filterTests);
    
    // Category card filtering
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            categoryFilter.value = category;
            filterTests();
            
            // Highlight selected category
            categoryCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Add animation to test cards on scroll
    const animateTestCards = function() {
        const cards = document.querySelectorAll('.test-card');
        
        cards.forEach((card, index) => {
            const rect = card.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
            
            if (isVisible && !card.classList.contains('animated')) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'all 0.5s ease';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                    card.classList.add('animated');
                }, index * 100);
            }
        });
    };
    
    window.addEventListener('scroll', animateTestCards);
    animateTestCards(); // Run once on page load
    
    // Add hover effect to category icons
    const categoryIcons = document.querySelectorAll('.category-icon');
    categoryIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.color = 'var(--primary-light)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.color = 'var(--primary-color)';
        });
    });
});