// Вкладкаларды басқару
function openTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`button[onclick="openTab('${tabId}')"]`).classList.add('active');
    
    // "Тапсырыстар" вкладкасы ашылғанда тізімді жаңарту
    if (tabId === 'all-orders') {
        displayOrders();
    }
}

// Модальды терезе
function openModal() {
    document.getElementById('orderModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('orderModal').style.display = 'none';
    // Форманы тазалау
    document.getElementById('order-title').value = '';
    document.getElementById('order-description').value = '';
}

// Тапсырысты сақтау
function saveOrder() {
    const title = document.getElementById('order-title').value;
    const description = document.getElementById('order-description').value;

    if (!title || !description) {
        alert('Барлық өрістерді толтырыңыз!');
        return;
    }

    // LocalStorage-дан бар тапсырыстарды алу
    let orders = JSON.parse(localStorage.getItem('orders')) || [];

    // Жаңа тапсырысты қосу
    orders.push({ title, description });

    // LocalStorage-ға сақтау
    localStorage.setItem('orders', JSON.stringify(orders));

    // Модальды жабу және форманы тазалау
    closeModal();

    // Тапсырыстар тізімін жаңарту
    displayOrders();
}

// Барлық тапсырыстарды көрсету
function displayOrders() {
    const ordersList = document.getElementById('orders-list');
    ordersList.innerHTML = ''; // Тізімді тазалау

    // LocalStorage-дан тапсырыстарды алу
    const orders = JSON.parse(localStorage.getItem('orders')) || [];

    if (orders.length === 0) {
        ordersList.innerHTML = '<p>Тапсырыстар жоқ</p>';
        return;
    }

    // Әр тапсырысты тізімге қосу
    orders.forEach(order => {
        const orderItem = document.createElement('div');
        orderItem.classList.add('order-item');
        orderItem.innerHTML = `
            <img src="https://img.icons8.com/ios-filled/50/ffffff/document--v1.png" alt="Document">
            <span>${order.title}: ${order.description}</span>
        `;
        ordersList.appendChild(orderItem);
    });
}

// Бастапқыда тапсырыстарды жүктеу
document.addEventListener('DOMContentLoaded', () => {
    displayOrders();
});