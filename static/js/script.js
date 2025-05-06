document.addEventListener('DOMContentLoaded', function () {
    // === Theme Toggle ===
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        const savedTheme = localStorage.getItem('theme');

        if (savedTheme) {
            document.documentElement.className = savedTheme;
            updateThemeIcon(savedTheme);
        }

        themeToggle.addEventListener('click', function () {
            const currentTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
            document.documentElement.className = currentTheme;
            localStorage.setItem('theme', currentTheme);
            updateThemeIcon(currentTheme);
        });

        function updateThemeIcon(theme) {
            if (!themeIcon) return;
            themeIcon.classList.toggle('fa-moon', theme === 'light');
            themeIcon.classList.toggle('fa-sun', theme === 'dark');
        }
    }

    // === Animate Elements on Scroll ===
    const animatedElements = document.querySelectorAll('.feature-card, .test-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });

    function animateOnScroll() {
        animatedElements.forEach(el => {
            const top = el.getBoundingClientRect().top;
            if (top < window.innerHeight / 1.2) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    }

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on page load
});

// === Score Circle Animation ===
document.addEventListener("DOMContentLoaded", function () {
    const circles = document.querySelectorAll(".score-circle");
    circles.forEach(circle => {
        const percent = parseInt(circle.dataset.percentage);
        const radius = 70;
        const circumference = 2 * Math.PI * radius;

        const progress = circle.querySelector(".progress-ring-circle-fill");
        if (!progress) return;

        progress.setAttribute("stroke-dasharray", circumference);
        const offset = circumference * (1 - percent / 100);
        progress.setAttribute("stroke-dashoffset", offset);
    });
});
