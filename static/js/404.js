document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle (inherited from main script)
    
    // Create stars
    const notFoundSection = document.querySelector('.not-found');
    const starCount = 50;
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        
        // Random properties
        const size = Math.random() * 3;
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const opacity = Math.random();
        const duration = 2 + Math.random() * 3;
        const delay = Math.random() * 5;
        
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${x}%`;
        star.style.top = `${y}%`;
        star.style.setProperty('--opacity', opacity);
        star.style.setProperty('--duration', `${duration}s`);
        star.style.animationDelay = `${delay}s`;
        
        notFoundSection.appendChild(star);
    }
    
    // Add floating animation to astronaut
    const astronaut = document.querySelector('.astronaut img');
    if (astronaut) {
        astronaut.style.animation = 'float 6s ease-in-out infinite';
    }
});