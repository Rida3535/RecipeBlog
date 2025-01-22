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

// Function to toggle the search bar visibility
function toggleSearchBar() {
    const searchForm = document.getElementById('search-form');
    
    if (searchForm.style.display === 'none' || searchForm.style.display === '') {
        searchForm.style.display = 'block'; // Show the search bar
    } else {
        searchForm.style.display = 'none'; // Hide the search bar
    }
}

// Function to filter recipes based on search input
function searchRecipes() {
    var input, filter, container, cards, cardTitle, i;
    input = document.getElementById('search-bar');
    filter = input.value.toLowerCase();
    container = document.getElementById('recipe-container');
    cards = container.getElementsByClassName('recipe-card');

    for (i = 0; i < cards.length; i++) {
        cardTitle = cards[i].getElementsByTagName("h3")[0];
        if (cardTitle) {
            if (cardTitle.innerText.toLowerCase().indexOf(filter) > -1) {
                cards[i].style.display = "";
            } else {
                cards[i].style.display = "none";
            }
        }
    }
}