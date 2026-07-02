// ══════════════════════════════════════════════════════════
// Theme Toggle – Ricette Deliziose
// Reads/writes localStorage, flips data-theme on <html>
// ══════════════════════════════════════════════════════════

(function () {
    const STORAGE_KEY = 'ricette-theme';

    // Apply saved theme immediately (runs before paint)
    function applySavedTheme() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    }

    // Toggle between light and dark
    function toggleTheme() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem(STORAGE_KEY, 'light');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem(STORAGE_KEY, 'dark');
        }
    }

    // Apply immediately
    applySavedTheme();

    // Bind toggle buttons once DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.theme-toggle').forEach(function (btn) {
            btn.addEventListener('click', toggleTheme);
        });

        // Inject Mobile Menu Button dynamically if it doesn't exist
        const container = document.querySelector('header .container');
        const nav = document.querySelector('header nav');
        if (container && nav && !document.getElementById('menu-btn')) {
            const menuBtn = document.createElement('button');
            menuBtn.id = 'menu-btn';
            menuBtn.className = 'menu-btn';
            menuBtn.setAttribute('aria-label', 'Toggle Navigation Menu');
            menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            
            // Append button inside container next to nav
            container.appendChild(menuBtn);

            // Toggle active state
            menuBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                nav.classList.toggle('active');
                if (nav.classList.contains('active')) {
                    menuBtn.innerHTML = '<i class="fas fa-times"></i>';
                } else {
                    menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                }
            });

            // Close nav when clicking outside
            document.addEventListener('click', function (e) {
                if (nav.classList.contains('active') && !nav.contains(e.target) && !menuBtn.contains(e.target)) {
                    nav.classList.remove('active');
                    menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                }
            });
        }
    });
})();
