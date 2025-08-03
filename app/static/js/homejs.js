// Global variables
let currentSlide = 0;
let isLoggedIn = false;
let userType = null;
let cartCount = 0;
let wishlistCount = 0;
let flashSaleTimer = null;

// Sample product data
const flashSaleProducts = [
    {
        id: 1,
        name: "Wireless Bluetooth Headphones with Noise Cancellation",
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=400&q=80",
        currentPrice: 79.99,
        originalPrice: 129.99,
        discount: 38,
        soldPercentage: 65,
        rating: 4.5,
        reviews: 1250
    },
    {
        id: 2,
        name: "Smart Fitness Watch with Heart Rate Monitor",
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=400&q=80",
        currentPrice: 149.99,
        originalPrice: 249.99,
        discount: 40,
        soldPercentage: 78,
        rating: 4.7,
        reviews: 892
    },
    {
        id: 3,
        name: "Premium Gaming Mechanical Keyboard",
        image: "https://images.unsplash.com/photo-1541140532154-b024d705b90a?auto=format&fit=crop&w=400&q=80",
        currentPrice: 89.99,
        originalPrice: 159.99,
        discount: 44,
        soldPercentage: 52,
        rating: 4.6,
        reviews: 634
    },
    {
        id: 4,
        name: "4K Ultra HD Webcam for Streaming",
        image: "https://images.unsplash.com/photo-1587831990711-23ca6441447b?auto=format&fit=crop&w=400&q=80",
        currentPrice: 119.99,
        originalPrice: 199.99,
        discount: 40,
        soldPercentage: 43,
        rating: 4.4,
        reviews: 456
    },
    {
        id: 5,
        name: "Portable Power Bank 20000mAh Fast Charging",
        image: "https://images.unsplash.com/photo-1609592358564-2b8f4f8bd0a1?auto=format&fit=crop&w=400&q=80",
        currentPrice: 34.99,
        originalPrice: 59.99,
        discount: 42,
        soldPercentage: 89,
        rating: 4.3,
        reviews: 1876
    }
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeCarousel();
    initializeAuth();
    initializeProducts();
    initializeCountdown();
    initializeEventListeners();
    setCarouselBackgrounds();
});

// Carousel functionality
function initializeCarousel() {
    const slides = document.querySelectorAll('.slide');
    const indicators = document.querySelectorAll('.indicator');
    
    // Auto-rotate slides every 5 seconds
    setInterval(() => {
        nextSlide();
    }, 5000);
    
    // Next slide function
    window.nextSlide = function() {
        slides[currentSlide].classList.remove('active');
        indicators[currentSlide].classList.remove('active');
        
        currentSlide = (currentSlide + 1) % slides.length;
        
        slides[currentSlide].classList.add('active');
        indicators[currentSlide].classList.add('active');
    };
    
    // Previous slide function
    window.prevSlide = function() {
        slides[currentSlide].classList.remove('active');
        indicators[currentSlide].classList.remove('active');
        
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        
        slides[currentSlide].classList.add('active');
        indicators[currentSlide].classList.add('active');
    };
    
    // Indicator click handlers
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            slides[currentSlide].classList.remove('active');
            indicators[currentSlide].classList.remove('active');
            
            currentSlide = index;
            
            slides[currentSlide].classList.add('active');
            indicators[currentSlide].classList.add('active');
        });
    });
}

// Set carousel backgrounds
function setCarouselBackgrounds() {
    const slides = document.querySelectorAll('.slide');
    slides.forEach(slide => {
        const bgImage = slide.getAttribute('data-bg');
        if (bgImage) {
            slide.style.backgroundImage = `url(${bgImage})`;
        }
    });
}

// Authentication functionality
function initializeAuth() {
    // Modal elements
    const authModal = document.getElementById('authModal');
    const registerPromptModal = document.getElementById('registerPromptModal');
    const closeBtns = document.querySelectorAll('.close');
    
    // Auth buttons
    const loginBtns = document.querySelectorAll('[id^="loginBtn"]');
    const cartBtns = document.querySelectorAll('.cart-btn');
    
    // Tab functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const authForms = document.querySelectorAll('.auth-form');
    
    // Login button click handlers
    loginBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (!isLoggedIn) {
                openModal('authModal');
            }
        });
    });
    
    // Cart button click handlers
    cartBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (!isLoggedIn) {
                openModal('registerPromptModal');
            } else {
                // Navigate to cart page
                showToast('Cart', 'Navigating to cart page...', 'info');
            }
        });
    });
    
    // Close button handlers
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal('authModal');
            closeModal('registerPromptModal');
        });
    });
    
    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            
            // Remove active class from all tabs and forms
            tabBtns.forEach(t => t.classList.remove('active'));
            authForms.forEach(f => f.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding form
            btn.classList.add('active');
            document.getElementById(tabName + 'Form').classList.add('active');
        });
    });
    
    // Password toggle functionality
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const passwordInput = btn.previousElementSibling;
            const icon = btn.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === authModal) {
            closeModal('authModal');
        }
        if (e.target === registerPromptModal) {
            closeModal('registerPromptModal');
        }
    });
}

// Modal functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Auth modal opening from register prompt
window.openAuthModal = function(type) {
    closeModal('registerPromptModal');
    openModal('authModal');
    
    // Switch to the appropriate tab
    const tabBtns = document.querySelectorAll('.tab-btn');
    const authForms = document.querySelectorAll('.auth-form');
    
    tabBtns.forEach(btn => btn.classList.remove('active'));
    authForms.forEach(form => form.classList.remove('active'));
    
    document.querySelector(`[data-tab="${type}"]`).classList.add('active');
    document.getElementById(type + 'Form').classList.add('active');
};

// Handle authentication
window.handleAuth = function(action, userTypeParam) {
    const email = action === 'login' ? 
        document.getElementById('loginEmail').value : 
        document.getElementById('registerEmail').value;
    
    const password = action === 'login' ? 
        document.getElementById('loginPassword').value : 
        document.getElementById('registerPassword').value;
    
    if (!email || !password) {
        showToast('Error', 'Please fill in all required fields', 'error');
        return;
    }
    
    // Simulate API call
    setTimeout(() => {
        isLoggedIn = true;
        userType = userTypeParam;
        
        // Update UI
        updateAuthUI();
        
        // Close modal
        closeModal('authModal');
        
        // Show success message
        showToast(
            action === 'login' ? 'Login Successful' : 'Registration Successful',
            `Welcome ${userType === 'seller' ? 'seller' : 'to our store'}!`,
            'success'
        );
        
        // Redirect seller to dashboard
        if (userType === 'seller') {
            setTimeout(() => {
                showToast('Seller Dashboard', 'Redirecting to your seller dashboard...', 'info');
            }, 1000);
        }
    }, 1000);
};

// Update authentication UI
function updateAuthUI() {
    const authBtns = document.querySelectorAll('.auth-btn');
    authBtns.forEach(btn => {
        if (isLoggedIn) {
            btn.innerHTML = '<i class="fas fa-user"></i><span>Account</span>';
        } else {
            btn.innerHTML = '<i class="fas fa-user"></i><span>Login</span>';
        }
    });
}

// Products functionality
function initializeProducts() {
    const productsGrid = document.getElementById('productsGrid');
    
    flashSaleProducts.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
}

// Create product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    card.innerHTML = `
        <div class="product-image">
            <img src="${product.image}" alt="${product.name}">
            <div class="discount-badge">-${product.discount}%</div>
            <button class="wishlist-btn-card" onclick="toggleWishlist(${product.id}, this)">
                <i class="fas fa-heart"></i>
            </button>
        </div>
        <div class="product-info">
            <div class="product-title">${product.name}</div>
            <div class="rating">
                <div class="stars">
                    ${generateStars(product.rating)}
                </div>
                <span class="reviews">(${product.reviews})</span>
            </div>
            <div class="price">
                <span class="current-price">$${product.currentPrice.toFixed(2)}</span>
                <span class="original-price">$${product.originalPrice.toFixed(2)}</span>
            </div>
            <div class="progress-info">
                <div class="progress-text">
                    <span class="sold-text">Sold: ${product.soldPercentage}%</span>
                    <span class="left-text">${100 - product.soldPercentage}% left</span>
                </div>
                <div class="progress-bar">
                    <div class="progress" style="width: ${product.soldPercentage}%"></div>
                </div>
            </div>
            <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                <i class="fas fa-shopping-cart"></i>
                Add to Cart
            </button>
        </div>
    `;
    
    return card;
}

// Generate star rating
function generateStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) {
            stars += '<i class="fas fa-star star"></i>';
        } else if (i - 0.5 <= rating) {
            stars += '<i class="fas fa-star-half-alt star"></i>';
        } else {
            stars += '<i class="fas fa-star star empty"></i>';
        }
    }
    return stars;
}

// Add to cart functionality
window.addToCart = function(productId) {
    if (!isLoggedIn) {
        openModal('registerPromptModal');
        return;
    }
    
    cartCount++;
    updateCartCount();
    showToast('Added to Cart', 'Product has been added to your cart successfully!', 'success');
};

// Toggle wishlist
window.toggleWishlist = function(productId, button) {
    if (!isLoggedIn) {
        showToast('Login Required', 'Please login to add items to your wishlist.', 'error');
        return;
    }
    
    button.classList.toggle('active');
    
    if (button.classList.contains('active')) {
        wishlistCount++;
        showToast('Added to Wishlist', 'Item added to your wishlist', 'success');
    } else {
        wishlistCount--;
        showToast('Removed from Wishlist', 'Item removed from your wishlist', 'info');
    }
    
    updateWishlistCount();
};

// Update cart count
function updateCartCount() {
    const cartCounts = document.querySelectorAll('#cartCount');
    cartCounts.forEach(count => {
        count.textContent = cartCount;
        count.style.display = cartCount > 0 ? 'flex' : 'none';
    });
}

// Update wishlist count
function updateWishlistCount() {
    const wishlistCounts = document.querySelectorAll('#wishlistCount');
    wishlistCounts.forEach(count => {
        count.textContent = wishlistCount;
        count.style.display = wishlistCount > 0 ? 'flex' : 'none';
    });
}

// Countdown timer functionality
function initializeCountdown() {
    let timeLeft = {
        hours: 12,
        minutes: 45,
        seconds: 30
    };
    
    function updateCountdown() {
        // Update timer display
        document.getElementById('hours').textContent = 
            timeLeft.hours.toString().padStart(2, '0');
        document.getElementById('minutes').textContent = 
            timeLeft.minutes.toString().padStart(2, '0');
        document.getElementById('seconds').textContent = 
            timeLeft.seconds.toString().padStart(2, '0');
        
        // Update timer in navigation
        const timerElement = document.getElementById('timer');
        if (timerElement) {
            timerElement.textContent = 
                `${timeLeft.hours.toString().padStart(2, '0')}:${timeLeft.minutes.toString().padStart(2, '0')}:${timeLeft.seconds.toString().padStart(2, '0')}`;
        }
        
        // Countdown logic
        if (timeLeft.seconds > 0) {
            timeLeft.seconds--;
        } else if (timeLeft.minutes > 0) {
            timeLeft.minutes--;
            timeLeft.seconds = 59;
        } else if (timeLeft.hours > 0) {
            timeLeft.hours--;
            timeLeft.minutes = 59;
            timeLeft.seconds = 59;
        } else {
            // Timer ended
            clearInterval(flashSaleTimer);
            showToast('Flash Sale Ended', 'The flash sale has ended. Check out our other deals!', 'info');
        }
    }
    
    // Update immediately and then every second
    updateCountdown();
    flashSaleTimer = setInterval(updateCountdown, 1000);
}

// Newsletter subscription
function initializeEventListeners() {
    // Newsletter subscription
    const subscribeBtn = document.getElementById('subscribeBtn');
    const newsletterEmail = document.getElementById('newsletterEmail');
    
    subscribeBtn.addEventListener('click', () => {
        const email = newsletterEmail.value;
        if (email && validateEmail(email)) {
            showToast('Subscribed!', 'Thank you for subscribing to our newsletter!', 'success');
            newsletterEmail.value = '';
        } else {
            showToast('Invalid Email', 'Please enter a valid email address', 'error');
        }
    });
    
    // Search functionality
    const searchBtns = document.querySelectorAll('.search-bar button');
    searchBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const searchInput = btn.previousElementSibling;
            const query = searchInput.value.trim();
            if (query) {
                showToast('Search', `Searching for: ${query}`, 'info');
            }
        });
    });
    
    // Category clicks
    const categoryItems = document.querySelectorAll('.category-item');
    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            const categoryName = item.querySelector('h3').textContent;
            showToast('Category', `Browsing ${categoryName} products`, 'info');
        });
    });
}

// Utility functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Toast notification system
function showToast(title, message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastIcon = toast.querySelector('.toast-icon');
    const toastTitle = toast.querySelector('.toast-title');
    const toastMessage = toast.querySelector('.toast-message');
    
    // Set content
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    // Set icon and type
    toast.className = `toast ${type}`;
    
    switch (type) {
        case 'success':
            toastIcon.className = 'fas fa-check-circle toast-icon';
            break;
        case 'error':
            toastIcon.className = 'fas fa-exclamation-circle toast-icon';
            break;
        case 'info':
            toastIcon.className = 'fas fa-info-circle toast-icon';
            break;
        default:
            toastIcon.className = 'fas fa-bell toast-icon';
    }
    
    // Show toast
    toast.classList.add('show');
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Navigation controls
document.querySelector('.carousel-control.prev').addEventListener('click', prevSlide);
document.querySelector('.carousel-control.next').addEventListener('click', nextSlide);

// Mobile menu toggle (for future enhancement)
document.querySelector('.category-menu').addEventListener('click', () => {
    showToast('Categories', 'Category menu clicked', 'info');
});

// Search enter key support
document.querySelectorAll('.search-bar input').forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = input.value.trim();
            if (query) {
                showToast('Search', `Searching for: ${query}`, 'info');
            }
        }
    });
});