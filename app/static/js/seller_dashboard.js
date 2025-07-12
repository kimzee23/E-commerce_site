document.addEventListener('DOMContentLoaded', () => {
  console.log("✅ Seller Dashboard JS Loaded");
});

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
    default:
      toastIcon.className = 'fas fa-info-circle toast-icon';
  }

  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

function submitProduct() {
  const form = document.getElementById('productForm');
  const formData = new FormData(form);

  const images = [];
  formData.getAll('images_url').forEach((url) => {
    if (url && url.trim()) images.push(url.trim());
  });

  if (images.length === 0) {
    showToast("Missing Image", "At least one image URL is required.", "error");
    return;
  }

  const payload = {
    name: formData.get('name'),
    description: formData.get('description'),
    price: parseFloat(formData.get('price')),
    category: formData.get('category'),
    stock_quantity: parseInt(formData.get('stock_quantity')),
    images_url: images,
    seller_id: localStorage.getItem('user_id')
  };

  fetch('/api/products', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
    },
    body: JSON.stringify(payload)
  })
  .then(async res => {
    const data = await res.json();
    if (res.ok) {
      showToast("Success", "Product uploaded successfully", "success");
      form.reset();
    } else {
      showToast("Upload Failed", data.message || "Error uploading product", "error");
    }
  })
  .catch(error => {
    console.error("Error:", error);
    showToast("Error", "Something went wrong while uploading", "error");
  });
}

function logout() {
  localStorage.clear();
  showToast("Logged Out", "You have been logged out.", "info");
  setTimeout(() => {
    window.location.href = "/";
  }, 1000);
}
