const role = localStorage.getItem('role');
localStorage.removeItem('pending_verification');

if (role === 'seller') {
  window.location.href = 'api/seller/dashboard';
} else {
  window.location.href = '/';
}
