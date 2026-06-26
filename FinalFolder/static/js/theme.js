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
    });
})();
