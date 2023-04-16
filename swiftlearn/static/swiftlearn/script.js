document.addEventListener('DOMContentLoaded', function () {
    const profileIcon = document.getElementById('profile-icon');
    const dropdownMenu = document.createElement('div');
    dropdownMenu.classList.add('hidden', 'absolute', 'right-0', 'top-14', 'bg-white', 'rounded-lg', 'shadow-lg', 'py-2');

    // Create the menu items
    const isAuthenticated = profileIcon.dataset.authenticated === 'True';
    const menuItems = isAuthenticated ? [
        { text: 'Dashboard', url: '#' },
        { text: 'Profile', url: '#' },
        { text: 'Logout', url: 'logout' }
    ] : [
        { text: 'Login', url: 'login' },
        { text: 'Register', url: 'register' }
    ];

    // Loop through the menu items and create links for each
    menuItems.forEach(item => {
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.text;
        link.classList.add('block', 'px-4', 'py-2', 'hover:bg-gray-200');
        dropdownMenu.appendChild(link);
    });

    // Append the dropdown menu to the profile icon
    profileIcon.appendChild(dropdownMenu);

    // Add a click event listener to the profile icon
    profileIcon.addEventListener('click', () => {
        dropdownMenu.classList.toggle('hidden');
    });

    // Add a click event listener to the document object
    document.addEventListener('click', (event) => {
        const isClickInsideDropdown = dropdownMenu.contains(event.target);
        const isClickInsideProfileIcon = profileIcon.contains(event.target);
        if (!isClickInsideDropdown && !isClickInsideProfileIcon) {
            dropdownMenu.classList.add('hidden');
        }
    });

    const hamburger = document.querySelector('.hamburger');
    const hamburgerMenu = document.querySelector('#dropdown-menu');

    hamburger.addEventListener('click', () => {
        hamburgerMenu.classList.toggle('hidden');
    });


    document.getElementById('sm-filter-btn').addEventListener('click', function() {
        const filterMenu = document.getElementById("filterMenu");
        filterMenu.classList.toggle("hidden");
    })
});
