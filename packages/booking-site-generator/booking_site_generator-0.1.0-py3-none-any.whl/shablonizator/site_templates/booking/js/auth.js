// Функция для проверки авторизации пользователя
function checkAuth() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const isAdminLoggedIn = localStorage.getItem('isAdminLoggedIn');
    
    // Получаем текущую страницу
    const currentPage = window.location.pathname.split('/').pop();
    
    // Страницы, требующие авторизации пользователя
    const userAuthPages = ['requests.html', 'new-request.html', 'profile.html'];
    
    // Страницы, требующие авторизации администратора
    const adminAuthPages = ['admin.html', 'admin-cars.html', 'admin-users.html'];
    
    // Страницы авторизации
    const authPages = ['login.html', 'registration.html'];
    
    // Редирект для неавторизованных пользователей
    if (userAuthPages.includes(currentPage) && !isLoggedIn) {
        window.location.href = 'login.html';
        return;
    }
    
    // Редирект для неавторизованных администраторов
    if (adminAuthPages.includes(currentPage) && !isAdminLoggedIn) {
        window.location.href = 'login.html';
        return;
    }
    
    // Редирект для авторизованных пользователей, пытающихся получить доступ к страницам авторизации
    if (authPages.includes(currentPage) && (isLoggedIn || isAdminLoggedIn)) {
        if (isAdminLoggedIn) {
            window.location.href = 'admin.html';
        } else {
            window.location.href = 'requests.html';
        }
        return;
    }
}

// Функция для выхода из системы
function logout() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('isAdminLoggedIn');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    
    window.location.href = 'login.html';
}

// Экспортируем функции в глобальную область видимости
window.checkAuth = checkAuth;
window.logout = logout;

// Проверка авторизации при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    
    // Добавляем обработчик для кнопки выхода, если она есть на странице
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
});