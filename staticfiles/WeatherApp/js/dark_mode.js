document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('dark-mode');
    const body = document.body;

    // Check if dark mode is enabled in the session
    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    // Set initial dark mode based on the session
    if (isDarkMode) {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }

    // Add event listener to the toggle button
    darkModeToggle.addEventListener('click', function() {
        // Toggle dark mode
        body.classList.toggle('dark-mode');

        // Save the dark mode state in the session
        const newDarkMode = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', newDarkMode);
    });
});

