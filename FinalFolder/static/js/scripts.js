// JavaScript for Recipe Blog

// Toggle Navigation Menu
const menuBtn = document.getElementById('menu-btn');
const nav = document.querySelector('nav');

if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
        nav.classList.toggle('active');
    });
}

// Smooth Scroll to Sections (only for local anchors starting with '#')
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', e => {
        const href = e.currentTarget.getAttribute('href');
        if (href && href.startsWith('#')) {
            const targetId = href.slice(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                if (nav) nav.classList.remove('active'); // Close menu on mobile
            }
        }
    });
});

// Function to toggle the visibility of the search bar
function toggleSearchBar() {
    const searchInput = document.getElementById('search-bar');
    if (searchInput.style.display === 'none' || searchInput.style.display === '') {
        searchInput.style.display = 'inline-block'; // Show the search input
        searchInput.focus();
    } else {
        searchInput.style.display = 'none'; // Hide the search input
    }
}

// Function to filter recipes based on the search input
function searchRecipes() {
    var input, filter, container, cards, cardTitle, i;
    input = document.getElementById('search-bar');
    filter = input.value.toLowerCase(); // Get search query in lowercase
    container = document.getElementById('recipe-container');
    cards = container.getElementsByClassName('recipe-card');

    // Loop through all recipe cards and display matching ones
    for (i = 0; i < cards.length; i++) {
        cardTitle = cards[i].getElementsByTagName("h3")[0]; // Get the title of each card
        if (cardTitle) {
            if (cardTitle.innerText.toLowerCase().indexOf(filter) > -1) {
                cards[i].style.display = ""; // Show card if it matches
            } else {
                cards[i].style.display = "none"; // Hide card if it doesn't match
            }
        }
    }
}

// Image Uploader
function showImagePreview(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (file) {
        const preview = document.getElementById('preview');
        const filename = document.getElementById('filename');
        
        // Show the filename
        filename.textContent = `Uploaded File: ${file.name}`;

        // Show the image preview
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

//like-btn
function likeRecipe(recipeId) {
    fetch(`/like_recipe/${recipeId}`, {
        method: "POST",  // Use POST instead of GET
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`like-btn-${recipeId}`).outerHTML = 
                `<span class="btn-liked" id="like-btn-${recipeId}" title="Liked"><i class="fas fa-heart"></i></span>`;
        } else {
            alert(data.message);
        }
    });
}

// Remove Flash Messages after 3 seconds
document.addEventListener("DOMContentLoaded", function() {
    let flashMessages = document.querySelectorAll(".alert");
    
    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = "0";
            setTimeout(() => message.remove(), 500);
        }, 3000);
    });
});
