document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle (inherited from main script)
    
    // Add animation to team members on scroll
    const animateTeamMembers = function() {
        const teamMembers = document.querySelectorAll('.team-member');
        
        teamMembers.forEach((member, index) => {
            const rect = member.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
            
            if (isVisible && !member.classList.contains('animated')) {
                member.style.opacity = '0';
                member.style.transform = 'translateY(20px)';
                member.style.transition = 'all 0.5s ease';
                
                setTimeout(() => {
                    member.style.opacity = '1';
                    member.style.transform = 'translateY(0)';
                    member.classList.add('animated');
                }, index * 100);
            }
        });
    };
    
    window.addEventListener('scroll', animateTeamMembers);
    animateTeamMembers(); // Run once on page load
    
    // Add hover effect to value cards
    const valueCards = document.querySelectorAll('.value-card');
    valueCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.value-icon');
            icon.style.transform = 'scale(1.2)';
            icon.style.color = 'var(--primary-light)';
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.value-icon');
            icon.style.transform = 'scale(1)';
            icon.style.color = 'var(--primary-color)';
        });
    });
});