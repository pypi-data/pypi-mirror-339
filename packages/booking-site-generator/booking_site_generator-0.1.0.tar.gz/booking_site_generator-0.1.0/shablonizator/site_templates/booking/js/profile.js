document.addEventListener('DOMContentLoaded', function() {
    // Проверка авторизации
    if (typeof window.checkAuth === 'function') {
        window.checkAuth();
    } else {
        // Если функция не определена, реализуем свою проверку
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        if (!isLoggedIn) {
            window.location.href = 'login.html';
            return; // Прекращаем выполнение, если нет авторизации
        }
    }
    
    // Проверяем, есть ли элементы формы на странице
    const profileForm = document.getElementById('profile-form');
    
    // Если формы нет на странице, прекращаем выполнение скрипта
    if (!profileForm) {
        console.log('Форма профиля не найдена на странице');
        return;
    }
    
    // Получаем остальные элементы
    const fullnameInput = document.getElementById('fullname');
    const phoneInput = document.getElementById('phone');
    const emailInput = document.getElementById('email');
    const licenseInput = document.getElementById('license');
    const passwordInput = document.getElementById('password');
    const newPasswordInput = document.getElementById('new-password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const passwordError = document.getElementById('password-error');
    const logoutBtn = document.getElementById('logout-btn');
    
    // Получаем данные пользователя
    const userEmail = localStorage.getItem('userEmail');
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const currentUser = users.find(user => user.email === userEmail);
    
    // Если пользователь найден, заполняем форму его данными
    if (currentUser) {
        fullnameInput.value = currentUser.fullname;
        phoneInput.value = currentUser.phone;
        emailInput.value = currentUser.email;
        licenseInput.value = currentUser.license;
    } else if (userEmail === 'test@example.com') {
        // Данные демо-пользователя
        fullnameInput.value = 'Тестовый Пользователь';
        phoneInput.value = '+7 (999) 888-77-66';
        emailInput.value = 'test@example.com';
        licenseInput.value = '7777 123456';
    }
    
    // Обработчик отправки формы (только если форма существует)
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Очищаем предыдущие ошибки
        passwordError.textContent = '';
        
        // Проверка текущего пароля
        if (currentUser && passwordInput.value !== currentUser.password) {
            passwordError.textContent = 'Неверный текущий пароль';
            return;
        }
        
        // Если введен новый пароль, проверяем его
        if (newPasswordInput.value) {
            if (newPasswordInput.value.length < 8) {
                passwordError.textContent = 'Новый пароль должен содержать не менее 8 символов';
                return;
            }
            
            if (newPasswordInput.value !== confirmPasswordInput.value) {
                passwordError.textContent = 'Новые пароли не совпадают';
                return;
            }
        }
        
        // Если пользователь не является тестовым, обновляем его данные
        if (currentUser) {
            // Обновляем данные пользователя
            currentUser.fullname = fullnameInput.value;
            currentUser.phone = phoneInput.value;
            currentUser.license = licenseInput.value;
            
            // Если введен новый пароль, обновляем его
            if (newPasswordInput.value) {
                currentUser.password = newPasswordInput.value;
            }
            
            // Сохраняем обновленные данные
            localStorage.setItem('users', JSON.stringify(users));
            localStorage.setItem('userName', currentUser.fullname);
            
            alert('Данные профиля успешно обновлены');
        } else {
            alert('Данные профиля тестового пользователя не могут быть изменены');
        }
    });
    }
    
    // Форматирование номера телефона при вводе (только если элемент существует)
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        if (value.length > 0) {
            if (value.length <= 1) {
                value = '+7 (' + value;
            } else if (value.length <= 4) {
                value = '+7 (' + value.substring(1, 4);
            } else if (value.length <= 7) {
                value = '+7 (' + value.substring(1, 4) + ') ' + value.substring(4, 7);
            } else if (value.length <= 9) {
                value = '+7 (' + value.substring(1, 4) + ') ' + value.substring(4, 7) + '-' + value.substring(7, 9);
            } else {
                value = '+7 (' + value.substring(1, 4) + ') ' + value.substring(4, 7) + '-' + value.substring(7, 9) + '-' + value.substring(9, 11);
            }
        }
        
        e.target.value = value;
    });
    }
    
    // Обработчик выхода из системы (только если кнопка существует)
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Очищаем данные авторизации
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        
        // Перенаправляем на страницу входа
        window.location.href = 'login.html';
    });
    }
});