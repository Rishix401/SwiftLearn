window.addEventListener('popstate', function(event) {
    signInBox = document.querySelector('#sign-in-div');
    forgetPasswordBox = document.querySelector('#forget-pass-div');

    // Update the UI based on the current URL
    const currentUrl = document.location.pathname;
    console.log(currentUrl)
    if (currentUrl === '/login') {
        signInBox.style.display = 'block';
        forgetPasswordBox.style.display = 'none';
    } else if (currentUrl === '/forget-password') {
        signInBox.style.display = 'none';
        forgetPasswordBox.style.display = 'block';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const profileIcon = document.getElementById('profile-icon');
    const dropdownMenu = document.createElement('div');
    dropdownMenu.classList.add('hidden', 'absolute', 'right-0', 'top-14', 'bg-white', 'rounded-lg', 'shadow-lg', 'py-2');

    // Create the menu items
    const isAuthenticated = profileIcon.dataset.authenticated === 'True';
    const menuItems = isAuthenticated ? [
        { text: 'Dashboard', url: '/dashboard' },
        { text: 'Profile', url: '/profile' },
        { text: 'Logout', url: '/logout' }
    ] : [
        { text: 'Login', url: '/login' },
        { text: 'Register', url: '/register' }
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

    try {
        document.getElementById('sm-filter-btn').addEventListener('click', function() {
            const filterMenu = document.getElementById("filterMenu");
            filterMenu.classList.toggle("hidden");
        })
    } catch(error) { console.log(error) }


    // Forget password logic
    try {
        signInBox = document.querySelector('#sign-in-div');
        signInBtn = document.querySelector('#sign-in-btn');
        forgetPasswordBox = document.querySelector('#forget-pass-div');
        forgetPasswordBtn = document.querySelector('#forget-password');
    
        forgetPasswordBox.style.display = 'none';
    
        forgetPasswordBtn.addEventListener('click', function() {
            history.pushState({}, '', '/forget-password');
            signInBox.style.display = 'none';
            forgetPasswordBox.style.display = 'block';
        })
    
        signInBtn.addEventListener('click', function() {
            history.pushState({}, '', '/login');
            signInBox.style.display = 'block';
            forgetPasswordBox.style.display = 'none';
        })
    } catch(error) { console.log(error) }

});
