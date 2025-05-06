document.addEventListener('DOMContentLoaded', function() {
    // Asosiy skriptdan mavzu almashish funksiyasini olish
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Yon menyu bo'limlari almashinuvi
    const menuItems = document.querySelectorAll('.menu-item');
    const settingsSections = document.querySelectorAll('.settings-section');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Faol menyu elementini o'zgartirish
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Tegishli bo'limni ko'rsatish
            const target = this.getAttribute('href').substring(1);
            settingsSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === `${target}-section`) {
                    section.classList.add('active');
                }
            });
        });
    });
    
    // Parolni o'zgartirish tugmasi
    const changePasswordBtn = document.getElementById('change-password');
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function() {
            // alert("Parolni o'zgartirish oynasi ochiladi!");
            // Haqiqiy loyihada bu modal oynani ochadi
        });
    }
    
    // Mavzu tanlovi tugmalari
    const themeOptions = document.querySelectorAll('.theme-option');
    themeOptions.forEach(option => {
        option.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            
            // Tanlangan mavzuni belgilash
            themeOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            
            // Mavzuni o'zgartirish
            if (theme === 'auto') {
                // Foydalanuvchi tizim mavzusiga moslash
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.documentElement.className = prefersDark ? 'dark' : 'light';
                localStorage.removeItem('theme');
            } else {
                document.documentElement.className = theme;
                localStorage.setItem('theme', theme);
            }
            
            // Mavzu ikonkasini yangilash
            updateThemeIcon(document.documentElement.className);
        });
    });
    
    // Mavzu ikonkasini yangilash funksiyasi
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    }
    
    // Toggle switcherlar uchun funksional
    const toggleSwitches = document.querySelectorAll('.switch input');
    toggleSwitches.forEach(switchEl => {
        switchEl.addEventListener('change', function() {
            const settingName = this.closest('.security-item, .notification-item, .privacy-item, .preference-item')
                                .querySelector('h3').textContent;
            console.log(`${settingName} sozlamasi ${this.checked ? 'yoqildi' : 'o\'chirildi'}`);
            // Haqiqiy loyihada bu sozlamalarni saqlash uchun API ga so'rov yuboriladi
        });
    });
    
    // Select elementlari uchun o'zgarishlarni kuzatish
    const selectElements = document.querySelectorAll('select');
    selectElements.forEach(select => {
        select.addEventListener('change', function() {
            const settingName = this.closest('.privacy-item, .preference-item')
                                .querySelector('h3').textContent;
            console.log(`${settingName} sozlamasi "${this.value}" qiymatiga o'zgartirildi`);
            // Haqiqiy loyihada bu sozlamalarni saqlash uchun API ga so'rov yuboriladi
        });
    });
    
    // Formani yuborish
    const settingsForm = document.querySelector('.settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // alert("Hisob ma'lumotlari muvaffaqiyatli yangilandi!");
            // Haqiqiy loyihada bu ma'lumotlarni saqlash uchun API ga so'rov yuboriladi
        });
    }
    
    // Sahifani yuklashda mavzuni tekshirish
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.className = savedTheme;
        updateThemeIcon(savedTheme);
        
        // Mavzu tanlovini belgilash
        themeOptions.forEach(option => {
            option.classList.remove('active');
            if (option.getAttribute('data-theme') === savedTheme) {
                option.classList.add('active');
            }
        });
    } else {
        // Avto mavzuni tanlash
        document.querySelector('.theme-option.auto').classList.add('active');
    }
});