// JavaScript for Recipe Blog

// Toggle Navigation Menu
const menuBtn = document.getElementById('menu-btn');
const nav = document.querySelector('nav');

menuBtn.addEventListener('click', () => {
    nav.classList.toggle('active');
});

// Smooth Scroll to Sections
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').slice(1);
        document.getElementById(targetId).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        nav.classList.remove('active'); // Close menu on mobile
    });
});

// Dynamic Recipe Cards
const recipe = [
    {
        title: "Spaghetti Bolognese",
        description: "A classic Italian pasta dish with a rich, meaty sauce.",
        image: "recipe1.jpg"
    },
    {
        title: "Chocolate Cake",
        description: "Moist and decadent chocolate cake for dessert lovers.",
        image: "recipe2.jpg"
    },
    {
        title: "Avocado Toast",
        description: "Healthy and delicious avocado toast with a twist.",
        image: "recipe3.jpg"
    }
];

const recipeContainer = document.getElementById('recipe-container');

recipes.forEach(recipe => {
    const recipeCard = document.createElement('div');
    recipeCard.classList.add('recipe-card');

    recipeCard.innerHTML = `
        <img src="${recipe.image}" alt="${recipe.title}">
        <h3>${recipe.title}</h3>
        <p>${recipe.description}</p>
        <a href="#" class="btn">View Recipe</a>
    `;

    recipeContainer.appendChild(recipeCard);
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
                `<span class="btn-liked">✔️Liked</span>`;
        } else {
            alert(data.message);
        }
    });
}