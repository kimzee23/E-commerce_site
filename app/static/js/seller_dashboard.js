// Seller Dashboard Full JS
let isLoggedIn = false;
let userType = null;

// On page load
window.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  isLoggedIn = Boolean(token);
  userType = role;

  if (!isLoggedIn || userType !== 'seller') {
    window.location.href = '/';
  }
});

// Submit Product
window.submitProduct = async function () {
  const token = localStorage.getItem('token');

  if (!token) {
    showToast('Error', 'You must be logged in as a seller.', 'error');
    return;
  }

  const form = document.getElementById('productForm');
  const formData = new FormData(form);

  const product = {
    name: formData.get('name').trim(),
    description: formData.get('description').trim(),
    price: parseFloat(formData.get('price')),
    category: formData.get('category').trim(),
    stock_quantity: parseInt(formData.get('stock_quantity')),
    images: formData.getAll('images_url').filter(url => url.trim() !== '')
  };

  if (!product.images || product.images.length === 0) {
    showToast('Error', 'Please provide at least one image URL.', 'error');
    return;
  }

  try {
    const res = await fetch('/api/products/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(product)
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error || 'Product upload failed');

    showToast('Success', 'Product uploaded successfully!', 'success');
    form.reset();
  } catch (err) {
    showToast('Upload Error', err.message, 'error');
  }
};

// Logout Function
window.logout = function () {
  localStorage.clear();
  window.location.href = '/';
};

// Toast Notification
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

// Close modal helper (if needed)
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.style.display = 'none';
}
