function showMessage(message, isError = false) {
  const messageBox = document.getElementById('cart-message');
  messageBox.textContent = message;
  messageBox.style.color = isError ? '#dc3545' : '#28a745';
  messageBox.style.display = 'block';

  setTimeout(() => {
    messageBox.style.display = 'none';
  }, 5000);
}

function updateQuantity(itemId, change) {
  const quantityElement = document.querySelector(`.cart-item[data-item-id="${itemId}"] .quantity-value`);
  const currentQuantity = parseInt(quantityElement.textContent);
  const newQuantity = currentQuantity + change;

  if (newQuantity < 1) {
    removeItem(itemId);
    return;
  }

  fetch(`${API_BASE_URL}/${CART_ID}/items/${itemId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      quantity: newQuantity
    })
  })
  .then(response => {
    if (!response.ok) throw new Error('Failed to update quantity');
    return response.json();
  })
  .then(updatedCart => {
    window.location.reload();
  })
  .catch(error => {
    showMessage(error.message, true);
    console.error('Error:', error);
  });
}

function removeItem(itemId) {
  if (!confirm('Are you sure you want to remove this item from your cart?')) return;

  fetch(`${API_BASE_URL}/${CART_ID}/items/${itemId}`, {
    method: 'DELETE'
  })
  .then(response => {
    if (!response.ok) throw new Error('Failed to remove item');
    return response.json();
  })
  .then(updatedCart => {
    window.location.reload();
  })
  .catch(error => {
    showMessage(error.message, true);
    console.error('Error:', error);
  });
}

function proceedToCheckout() {
  fetch(`${API_BASE_URL}/${CART_ID}/checkout`, {
    method: 'POST'
  })
  .then(response => {
    if (!response.ok) throw new Error('Checkout failed');
    return response.json();
  })
  .then(data => {
    window.location.href = data.redirectUrl || '/checkout';
  })
  .catch(error => {
    showMessage(error.message, true);
    console.error('Error:', error);
  });
}