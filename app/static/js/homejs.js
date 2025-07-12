// Homepage Script with Auth + Backend Integration
let currentSlide = 0;
let isLoggedIn = !!localStorage.getItem('token');
let userType = localStorage.getItem('role');
let cartCount = 0;
let wishlistCount = 0;
let flashSaleTimer = null;

// On load, check for user role and redirect accordingly
document.addEventListener('DOMContentLoaded', () => {
  const role = localStorage.getItem('role');
  const token = localStorage.getItem('token');

  if (role === 'seller') {
    window.location.href = '/seller/dashboard';
    return;
  }

  updateAuthUI();
  initializeCarousel();
  initializeAuth();
  initializeCountdown();
  initializeEventListeners();
  setCarouselBackgrounds();
});

// Handle login/register with real backend API and toasts
window.handleAuth = async function(action, userTypeParam) {
  const emailInput = document.getElementById(`${action}Email`);
  const passwordInput = document.getElementById(`${action}Password`);
  const nameInput = document.getElementById(`${action}Name`);
  const phoneInput = document.getElementById(`${action}Phone`);

  const email = emailInput?.value.trim();
  const password = passwordInput?.value.trim();
  const name = nameInput?.value.trim() || '';
  const phone = phoneInput?.value.trim() || '';

  if (!email || !password || (action === 'register' && (!name || !phone))) {
    showToast('Error', 'Please fill in all required fields.', 'error');
    return;
  }

  const endpoint = userTypeParam === 'seller' ? '/api/sellers' : '/api/customers';
  const url = action === 'register' ? `${endpoint}/register` : `${endpoint}/login`;

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name, phone })
    });

    const data = await res.json();

    if (res.status === 409) {
      showToast('Already Registered', data.message || 'User already exists.', 'info');
      return;
    }

    if (!res.ok) {
      showToast('Authentication Failed', data.message || 'Invalid credentials or request.', 'error');
      return;
    }

    localStorage.setItem('token', data.token);
    localStorage.setItem('role', userTypeParam);
    localStorage.setItem('user_id', data.user_id);

    isLoggedIn = true;
    userType = userTypeParam;

    updateAuthUI();
    closeModal('authModal');

    showToast(
      action === 'login' ? 'Login Successful' : 'Registration Successful',
      `Welcome ${userTypeParam === 'seller' ? 'Seller' : 'Buyer'}!`,
      'success'
    );

    setTimeout(() => {
      window.location.href = userTypeParam === 'seller' ? '/seller/dashboard' : '/dashboard';
    }, 1500);

  } catch (err) {
    showToast('Error', err.message || 'Something went wrong. Try again.', 'error');
  }
};

// Redirect user to appropriate dashboard
function updateAuthUI() {
  const authBtns = document.querySelectorAll('.auth-btn');
  authBtns.forEach(btn => {
    btn.innerHTML = isLoggedIn ? '<i class="fas fa-user"></i><span>Account</span>' : '<i class="fas fa-user"></i><span>Login</span>';
  });
}

// Utility toast function
function showToast(title, message, type = 'info') {
  const toast = document.getElementById('toast');
  const toastIcon = toast.querySelector('.toast-icon');
  const toastTitle = toast.querySelector('.toast-title');
  const toastMessage = toast.querySelector('.toast-message');

  toastTitle.textContent = title;
  toastMessage.textContent = message;

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

  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// Close modal helper
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.style.display = 'none';
}

// Carousel setup
function initializeCarousel() {
  const slides = document.querySelectorAll('.slide');
  const indicators = document.querySelectorAll('.indicator');

  setInterval(() => {
    nextSlide();
  }, 5000);

  window.nextSlide = function () {
    slides[currentSlide].classList.remove('active');
    indicators[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');
  };

  window.prevSlide = function () {
    slides[currentSlide].classList.remove('active');
    indicators[currentSlide].classList.remove('active');
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');
  };

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

function setCarouselBackgrounds() {
  const slides = document.querySelectorAll('.slide');
  slides.forEach(slide => {
    const bgImage = slide.getAttribute('data-bg');
    if (bgImage) {
      slide.style.backgroundImage = `url(${bgImage})`;
    }
  });
}

function initializeAuth() {
  const authModal = document.getElementById('authModal');
  const registerPromptModal = document.getElementById('registerPromptModal');
  const closeBtns = document.querySelectorAll('.close');

  const loginBtns = document.querySelectorAll('[id^="loginBtn"]');
  const cartBtns = document.querySelectorAll('.cart-btn');

  const tabBtns = document.querySelectorAll('.tab-btn');
  const authForms = document.querySelectorAll('.auth-form');

  loginBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (!isLoggedIn) openModal('authModal');
    });
  });

  cartBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (!isLoggedIn) {
        openModal('registerPromptModal');
      } else {
        showToast('Cart', 'Navigating to cart page...', 'info');
      }
    });
  });

  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      closeModal('authModal');
      closeModal('registerPromptModal');
    });
  });

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.getAttribute('data-tab');
      tabBtns.forEach(t => t.classList.remove('active'));
      authForms.forEach(f => f.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(tabName + 'Form').classList.add('active');
    });
  });

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

  window.addEventListener('click', (e) => {
    if (e.target === authModal) closeModal('authModal');
    if (e.target === registerPromptModal) closeModal('registerPromptModal');
  });
}

function openModal(modalId) {
  document.getElementById(modalId).style.display = 'block';
}

function initializeCountdown() {
  let timeLeft = { hours: 12, minutes: 45, seconds: 30 };

  function updateCountdown() {
    document.getElementById('hours').textContent = String(timeLeft.hours).padStart(2, '0');
    document.getElementById('minutes').textContent = String(timeLeft.minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(timeLeft.seconds).padStart(2, '0');

    const timerElement = document.getElementById('timer');
    if (timerElement) {
      timerElement.textContent = `${String(timeLeft.hours).padStart(2, '0')}:${String(timeLeft.minutes).padStart(2, '0')}:${String(timeLeft.seconds).padStart(2, '0')}`;
    }

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
      clearInterval(flashSaleTimer);
      showToast('Flash Sale Ended', 'The flash sale has ended. Check out our other deals!', 'info');
    }
  }

  updateCountdown();
  flashSaleTimer = setInterval(updateCountdown, 1000);
}

function initializeEventListeners() {
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

  const categoryItems = document.querySelectorAll('.category-item');
  categoryItems.forEach(item => {
    item.addEventListener('click', () => {
      const categoryName = item.querySelector('h3').textContent;
      showToast('Category', `Browsing ${categoryName} products`, 'info');
    });
  });

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

  document.querySelector('.carousel-control.prev').addEventListener('click', prevSlide);
  document.querySelector('.carousel-control.next').addEventListener('click', nextSlide);

  document.querySelector('.category-menu').addEventListener('click', () => {
    showToast('Categories', 'Category menu clicked', 'info');
  });
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}
async function loadProducts() {
  try {
    const res = await fetch('/api/v1/products');
    const data = await res.json();

    const grid = document.getElementById('productsGrid');
    grid.innerHTML = ''; // Clear any previous content

    if (Array.isArray(data) && data.length > 0) {
      data.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';

        productCard.innerHTML = `
          <div class="product-image">
            <img src="${product.images_url?.[0] || 'https://via.placeholder.com/150'}" alt="${product.name}">
          </div>
          <div class="product-info">
            <h4>${product.name}</h4>
            <p>$${product.price.toFixed(2)}</p>
            <button class="btn btn-primary add-to-cart-btn" data-id="${product._id}">Add to Cart</button>
          </div>
        `;

        grid.appendChild(productCard);
      });

      // Optional: Add event listeners to "Add to Cart"
      document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', (e) => {
          if (!isLoggedIn) {
            openModal('registerPromptModal');
          } else {
            showToast('Cart', 'Item added to cart (not yet saved)', 'success');
            cartCount++;
            document.getElementById('cartCount').textContent = cartCount;
          }
        });
      });

    } else {
      grid.innerHTML = `<p>No products found. Please check back later.</p>`;
    }

  } catch (err) {
    showToast('Error', 'Failed to load products. Try again.', 'error');
  }
}
