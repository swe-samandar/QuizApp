document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.className = savedTheme;
        updateThemeIcon(savedTheme);
    }
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        document.documentElement.className = currentTheme;
        localStorage.setItem('theme', currentTheme);
        updateThemeIcon(currentTheme);
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    }
    
    // Modal Handling
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    const closeModalBtns = document.querySelectorAll('.close-modal');
    const switchToRegister = document.getElementById('switch-to-register');
    const switchToLogin = document.getElementById('switch-to-login');
    
    loginBtn.addEventListener('click', function() {
        loginModal.classList.add('active');
    });
    
    registerBtn.addEventListener('click', function() {
        registerModal.classList.add('active');
    });
    
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            loginModal.classList.remove('active');
            registerModal.classList.remove('active');
        });
    });
    
    switchToRegister.addEventListener('click', function(e) {
        e.preventDefault();
        loginModal.classList.remove('active');
        registerModal.classList.add('active');
    });
    
    switchToLogin.addEventListener('click', function(e) {
        e.preventDefault();
        registerModal.classList.remove('active');
        loginModal.classList.add('active');
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === loginModal) {
            loginModal.classList.remove('active');
        }
        if (e.target === registerModal) {
            registerModal.classList.remove('active');
        }
    });
    
    // Form Validation
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    // Login Form Validation
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        let isValid = true;
        
        // Email validation
        const email = document.getElementById('login-email');
        const emailError = document.getElementById('login-email-error');
        if (!email.value || !validateEmail(email.value)) {
            emailError.textContent = 'Please enter a valid email address';
            emailError.style.display = 'block';
            isValid = false;
        } else {
            emailError.style.display = 'none';
        }
        
        // Password validation
        const password = document.getElementById('login-password');
        const passwordError = document.getElementById('login-password-error');
        if (!password.value || password.value.length < 6) {
            passwordError.textContent = 'Password must be at least 6 characters';
            passwordError.style.display = 'block';
            isValid = false;
        } else {
            passwordError.style.display = 'none';
        }
        
        if (isValid) {
            // Simulate login success
            alert('Login successful! Redirecting to dashboard...');
            loginModal.classList.remove('active');
            // In a real app, you would redirect to dashboard.html
            // window.location.href = 'dashboard.html';
        }
    });
    
    // Register Form Validation
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        let isValid = true;
        
        // Name validation
        const name = document.getElementById('register-name');
        const nameError = document.getElementById('register-name-error');
        if (!name.value || name.value.length < 3) {
            nameError.textContent = 'Name must be at least 3 characters';
            nameError.style.display = 'block';
            isValid = false;
        } else {
            nameError.style.display = 'none';
        }
        
        // Email validation
        const email = document.getElementById('register-email');
        const emailError = document.getElementById('register-email-error');
        if (!email.value || !validateEmail(email.value)) {
            emailError.textContent = 'Please enter a valid email address';
            emailError.style.display = 'block';
            isValid = false;
        } else {
            emailError.style.display = 'none';
        }
        
        // Password validation
        const password = document.getElementById('register-password');
        const passwordError = document.getElementById('register-password-error');
        if (!password.value || password.value.length < 8) {
            passwordError.textContent = 'Password must be at least 8 characters';
            passwordError.style.display = 'block';
            isValid = false;
        } else {
            passwordError.style.display = 'none';
        }
        
        // Confirm password validation
        const confirm = document.getElementById('register-confirm');
        const confirmError = document.getElementById('register-confirm-error');
        if (confirm.value !== password.value) {
            confirmError.textContent = 'Passwords do not match';
            confirmError.style.display = 'block';
            isValid = false;
        } else {
            confirmError.style.display = 'none';
        }
        
        // Terms agreement validation
        const terms = document.getElementById('terms-agree');
        if (!terms.checked) {
            alert('You must agree to the terms and conditions');
            isValid = false;
        }
        
        if (isValid) {
            // Simulate registration success
            alert('Registration successful! You can now login.');
            registerModal.classList.remove('active');
            loginModal.classList.add('active');
        }
    });
    
    // Email validation helper
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .test-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animation
    const animatedElements = document.querySelectorAll('.feature-card, .test-card');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on page load
});



document.addEventListener("DOMContentLoaded", function () {
    const circles = document.querySelectorAll(".score-circle");
    circles.forEach(circle => {
        const percent = parseInt(circle.dataset.percentage);
        const radius = 70;
        const circumference = 2 * Math.PI * radius;

        const progress = circle.querySelector(".progress-ring-circle-fill");
        progress.setAttribute("stroke-dasharray", circumference);
        const offset = circumference * (1 - percent / 100);
        progress.setAttribute("stroke-dashoffset", offset);
    });
});
