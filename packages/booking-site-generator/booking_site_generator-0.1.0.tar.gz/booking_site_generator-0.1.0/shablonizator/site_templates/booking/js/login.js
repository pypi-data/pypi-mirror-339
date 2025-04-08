document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы формы
    const loginForm = document.getElementById('login-form');
    
    // Проверяем, есть ли форма на странице
    if (!loginForm) {
        console.log('Форма входа не найдена на странице');
        return;
    }
    
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('login-error');
    
    // Обработка отправки формы
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Очищаем предыдущие ошибки
        if (loginError) {
            loginError.textContent = '';
        }
        
        // Получаем значения полей
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        
        // Проверка на пустые поля
        if (!email || !password) {
            if (loginError) {
                loginError.textContent = 'Пожалуйста, введите email и пароль';
            }
            return;
        }
        
        // Проверка на административный доступ
        if (email === 'admin@mail.ru' && password === 'admin123') {
            localStorage.setItem('isAdminLoggedIn', true);
            window.location.href = 'admin.html';
            return;
        }
        
        // Для демонстрационного аккаунта
        if (email === 'test@example.com' && password === 'password') {
            localStorage.setItem('isLoggedIn', true);
            localStorage.setItem('userEmail', email);
            localStorage.setItem('userName', 'Тестовый Пользователь');
            window.location.href = 'requests.html';
            return;
        }
        
        // Получаем зарегистрированных пользователей из хранилища
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        
        // Проверяем данные для входа
        const user = users.find(user => user.email === email && user.password === password);
        
        if (user) {
            // Сохраняем данные пользователя в localStorage
            localStorage.setItem('isLoggedIn', true);
            localStorage.setItem('userEmail', user.email);
            localStorage.setItem('userName', user.fullname);
            
            // Перенаправляем на страницу заявок
            window.location.href = 'requests.html';
        } else {
            // Выводим ошибку
            if (loginError) {
                loginError.textContent = 'Неверный email или пароль';
            }
        }
    });
    
    // Функция проверки авторизации (можно использовать на других страницах)
    function checkAuth() {
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        const isAdminLoggedIn = localStorage.getItem('isAdminLoggedIn');
        
        // Проверяем на каких страницах находится пользователь
        const currentPage = window.location.pathname.split('/').pop();
        
        // Страницы, требующие авторизации пользователя
        const userAuthPages = ['requests.html', 'new-request.html', 'profile.html'];
        
        // Страницы, требующие авторизации администратора
        const adminAuthPages = ['admin.html', 'admin-cars.html', 'admin-users.html'];
        
        if (userAuthPages.includes(currentPage) && !isLoggedIn) {
            window.location.href = 'login.html';
        }
        
        if (adminAuthPages.includes(currentPage) && !isAdminLoggedIn) {
            window.location.href = 'login.html';
        }
    }
    
    // Экспортируем функцию для использования в других модулях
    window.checkAuth = checkAuth;
});