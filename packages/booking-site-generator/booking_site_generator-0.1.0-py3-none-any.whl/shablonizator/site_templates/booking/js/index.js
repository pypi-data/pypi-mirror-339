document.addEventListener('DOMContentLoaded', function() {
    // Получаем элемент навигации
    const navLinks = document.getElementById('nav-links');
    
    // Проверяем статус авторизации
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const isAdminLoggedIn = localStorage.getItem('isAdminLoggedIn');
    
    // Формируем навигационные ссылки в зависимости от статуса авторизации
    if (isAdminLoggedIn) {
        // Ссылки для администратора
        navLinks.innerHTML = `
            <li><a href="admin.html">Админ-панель</a></li>
            <li><a href="#" id="logout-btn">Выйти</a></li>
        `;
    } else if (isLoggedIn) {
        // Ссылки для авторизованного пользователя
        navLinks.innerHTML = `
            <li><a href="requests.html">Мои заявки</a></li>
            <li><a href="new-request.html">Новая заявка</a></li>
            <li><a href="profile.html">Профиль</a></li>
            <li><a href="#" id="logout-btn">Выйти</a></li>
        `;
    } else {
        // Ссылки для гостя
        navLinks.innerHTML = `
            <li><a href="login.html">Войти</a></li>
            <li><a href="registration.html">Регистрация</a></li>
        `;
    }
    
    // Добавляем обработчик для кнопки выхода
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Очищаем данные авторизации
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('isAdminLoggedIn');
            
            // Перезагружаем страницу
            window.location.reload();
        });
    }
    
    // Обновляем ссылки на бронирование в карточках автомобилей
    updateBookingLinks();
    
    // Функция обновления ссылок бронирования
    function updateBookingLinks() {
        const bookingLinks = document.querySelectorAll('.car-card .btn');
        
        bookingLinks.forEach(link => {
            if (isLoggedIn) {
                // Если пользователь авторизован, направляем на страницу создания заявки
                link.href = 'new-request.html';
            } else {
                // Если не авторизован, направляем на страницу входа
                link.href = 'login.html';
            }
        });
    }
});