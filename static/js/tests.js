document.addEventListener('DOMContentLoaded', function () {
    // === View Toggle (List/Grid) ===
    const viewButtons = document.querySelectorAll('.view-btn');
    const testView = document.getElementById('test-view');

    if (viewButtons.length && testView) {
        viewButtons.forEach(button => {
            button.addEventListener('click', function () {
                viewButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                const viewType = this.getAttribute('data-view');
                testView.className = viewType === 'list' ? 'test-list-view' : 'test-grid';
            });
        });
    }

    // === Filtering by Category and Difficulty ===
    const categoryFilter = document.getElementById('category-filter');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const testCards = document.querySelectorAll('.test-card');
    const categoryCards = document.querySelectorAll('.category-card');

    function filterTests() {
        const selectedCategory = categoryFilter?.value;
        const selectedDifficulty = difficultyFilter?.value;

        testCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            const cardDifficulty = card.getAttribute('data-difficulty');

            const matchCategory = !selectedCategory || cardCategory === selectedCategory;
            const matchDifficulty = !selectedDifficulty || cardDifficulty === selectedDifficulty;

            card.style.display = matchCategory && matchDifficulty ? 'block' : 'none';
        });
    }

    if (categoryFilter && difficultyFilter) {
        categoryFilter.addEventListener('change', filterTests);
        difficultyFilter.addEventListener('change', filterTests);
    }

    if (categoryCards.length) {
        categoryCards.forEach(card => {
            card.addEventListener('click', function () {
                const category = this.getAttribute('data-category');
                if (categoryFilter) {
                    categoryFilter.value = category;
                    filterTests();
                }

                categoryCards.forEach(c => c.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }

    // === Animate test cards on scroll ===
    const animateTestCards = () => {
        document.querySelectorAll('.test-card').forEach((card, index) => {
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
    animateTestCards(); // Run on load

    // === Category Icon Hover Animation ===
    const categoryIcons = document.querySelectorAll('.category-icon');
    categoryIcons.forEach(icon => {
        icon.addEventListener('mouseenter', () => {
            icon.style.transform = 'scale(1.1)';
            icon.style.color = 'var(--primary-light)';
        });
        icon.addEventListener('mouseleave', () => {
            icon.style.transform = 'scale(1)';
            icon.style.color = 'var(--primary-color)';
        });
    });
});
