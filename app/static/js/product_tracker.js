// Global variables
let viewsChart, purchasesChart;
let allProductsData = [];

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize date pickers with default range (last 30 days)
    const today = new Date();
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    document.getElementById('dateFrom').valueAsDate = thirtyDaysAgo;
    document.getElementById('dateTo').valueAsDate = today;

    // Initialize charts
    initializeCharts();

    // Load data
    loadProductTrackerData();

    // Set up event listeners
    document.getElementById('applyDateRange').addEventListener('click', function() {
        loadProductTrackerData();
    });
});

function initializeCharts() {
    const viewsCtx = document.getElementById('viewsChart').getContext('2d');
    const purchasesCtx = document.getElementById('purchasesChart').getContext('2d');

    viewsChart = new Chart(viewsCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Views',
                data: [],
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: getChartOptions('Product Views Over Time')
    });

    purchasesChart = new Chart(purchasesCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Purchases',
                data: [],
                backgroundColor: 'rgba(16, 185, 129, 0.6)',
                borderColor: 'rgba(16, 185, 129, 1)',
                borderWidth: 1
            }]
        },
        options: getChartOptions('Product Purchases Over Time')
    });
}

function getChartOptions(title) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false,
                text: title
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    drawBorder: false
                },
                ticks: {
                    stepSize: 1
                }
            }
        }
    };
}

async function loadProductTrackerData() {
    const dateFrom = document.getElementById('dateFrom').value;
    const dateTo = document.getElementById('dateTo').value;

    try {
        // In a real app, you would fetch this from your Flask API
        // const response = await fetch(`/api/product-analytics?from=${dateFrom}&to=${dateTo}`);
        // allProductsData = await response.json();

        // For demo purposes, we'll use mock data
        allProductsData = generateMockData(dateFrom, dateTo);

        updateSummaryCards();
        updateCharts();
        updateProductTable();
    } catch (error) {
        console.error('Error loading product tracker data:', error);
        alert('Failed to load product analytics data');
    }
}

function updateSummaryCards() {
    const totalViews = allProductsData.reduce((sum, product) => sum + product.views, 0);
    const totalPurchases = allProductsData.reduce((sum, product) => sum + product.purchases, 0);
    const conversionRate = totalViews > 0 ? (totalPurchases / totalViews * 100).toFixed(1) : 0;

    // Find most recent dates
    const lastViewed = new Date(Math.max(...allProductsData.map(p => new Date(p.last_viewed))));
    const lastPurchased = new Date(Math.max(...allProductsData.map(p => new Date(p.last_purchased))));

    document.getElementById('totalViews').textContent = totalViews.toLocaleString();
    document.getElementById('totalPurchases').textContent = totalPurchases.toLocaleString();
    document.getElementById('conversionRate').textContent = `${conversionRate}%`;
    document.getElementById('lastViewed').textContent = formatDate(lastViewed);
    document.getElementById('lastPurchased').textContent = formatDate(lastPurchased);
}

function updateCharts() {
    // Group data by date for the charts
    const dateMap = {};

    allProductsData.forEach(product => {
        const viewedDate = new Date(product.last_viewed).toISOString().split('T')[0];
        const purchasedDate = new Date(product.last_purchased).toISOString().split('T')[0];

        // Count views
        if (!dateMap[viewedDate]) {
            dateMap[viewedDate] = { views: 0, purchases: 0 };
        }
        dateMap[viewedDate].views += product.views;

        // Count purchases
        if (!dateMap[purchasedDate]) {
            dateMap[purchasedDate] = { views: 0, purchases: 0 };
        }
        dateMap[purchasedDate].purchases += product.purchases;
    });

    // Sort dates chronologically
    const sortedDates = Object.keys(dateMap).sort();

    // Prepare chart data
    const viewsData = sortedDates.map(date => dateMap[date].views);
    const purchasesData = sortedDates.map(date => dateMap[date].purchases);

    // Update charts
    viewsChart.data.labels = sortedDates;
    viewsChart.data.datasets[0].data = viewsData;
    viewsChart.update();

    purchasesChart.data.labels = sortedDates;
    purchasesChart.data.datasets[0].data = purchasesData;
    purchasesChart.update();
}

function updateProductTable() {
    const tableBody = document.getElementById('productTableBody');
    tableBody.innerHTML = '';

    allProductsData.forEach(product => {
        const conversionRate = product.views > 0
            ? (product.purchases / product.views * 100).toFixed(1)
            : 0;

        const row = document.createElement('tr');

        // Determine conversion rate class
        let conversionClass = 'conversion-low';
        if (conversionRate > 5) conversionClass = 'conversion-medium';
        if (conversionRate > 10) conversionClass = 'conversion-high';

        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                        <img class="h-10 w-10 rounded-full" src="${product.image_url || '/static/images/placeholder.png'}" alt="">
                    </div>
                    <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">${product.name}</div>
                        <div class="text-sm text-gray-500">${product.category || 'N/A'}</div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${product.views}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${product.purchases}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${formatDate(new Date(product.last_viewed))}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${formatDate(new Date(product.last_purchased))}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium ${conversionClass}">${conversionRate}%</td>
        `;

        tableBody.appendChild(row);
    });
}

function formatDate(date) {
    if (!date) return 'Never';
    return moment(date).format('MMM D, YYYY h:mm A');
}

// Mock data generator for demonstration
function generateMockData(dateFrom, dateTo) {
    const mockProducts = [
        { _id: '1', name: 'Wireless Headphones', category: 'Electronics', image_url: '/static/images/headphones.jpg' },
        { _id: '2', name: 'Smart Watch', category: 'Electronics', image_url: '/static/images/smartwatch.jpg' },
        { _id: '3', name: 'Running Shoes', category: 'Sports', image_url: '/static/images/shoes.jpg' },
        { _id: '4', name: 'Coffee Maker', category: 'Home', image_url: '/static/images/coffee.jpg' },
        { _id: '5', name: 'Backpack', category: 'Travel', image_url: '/static/images/backpack.jpg' }
    ];

    const startDate = new Date(dateFrom);
    const endDate = new Date(dateTo);

    return mockProducts.map(product => {
        // Generate random view and purchase counts (1-1000)
        const views = Math.floor(Math.random() * 1000) + 1;
        const purchases = Math.floor(views * (Math.random() * 0.15)); // 0-15% conversion

        // Generate random last viewed/purchased dates within range
        const randomViewDate = new Date(startDate.getTime() + Math.random() * (endDate.getTime() - startDate.getTime()));
        const randomPurchaseDate = purchases > 0
            ? new Date(randomViewDate.getTime() + Math.random() * (endDate.getTime() - randomViewDate.getTime()))
            : null;

        return {
            product_id: product._id,
            name: product.name,
            category: product.category,
            image_url: product.image_url,
            views: views,
            purchases: purchases,
            last_viewed: randomViewDate.toISOString(),
            last_purchased: randomPurchaseDate ? randomPurchaseDate.toISOString() : null
        };
    });
}