document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы формы
    const registrationForm = document.getElementById('registration-form');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const passwordError = document.getElementById('password-error');
    const phoneInput = document.getElementById('phone');

    // Обработка отправки формы
    registrationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Очищаем предыдущие ошибки
        passwordError.textContent = '';
        
        // Проверка совпадения паролей
        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordError.textContent = 'Пароли не совпадают';
            return;
        }
        
        // Проверка сложности пароля
        if (passwordInput.value.length < 8) {
            passwordError.textContent = 'Пароль должен содержать не менее 8 символов';
            return;
        }
        
        // Получаем значения полей
        const fullname = document.getElementById('fullname').value;
        const phone = phoneInput.value;
        const email = document.getElementById('email').value;
        const password = passwordInput.value;
        const license = document.getElementById('license').value;
        
        // Проверяем, существует ли уже такой пользователь
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const existingUser = users.find(user => user.email === email);
        
        if (existingUser) {
            passwordError.textContent = 'Пользователь с таким email уже зарегистрирован';
            return;
        }
        
        // Создаем нового пользователя
        const newUser = {
            fullname,
            phone,
            email,
            password, // В реальном приложении пароль должен быть захеширован
            license,
            registrationDate: new Date().toISOString()
        };
        
        // Добавляем пользователя в хранилище
        users.push(newUser);
        localStorage.setItem('users', JSON.stringify(users));
        
        // Выводим сообщение об успешной регистрации и перенаправляем
        alert('Регистрация успешна! Теперь вы можете войти в систему.');
        window.location.href = 'login.html';
    });
    
    // Форматирование номера телефона при вводе
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
});document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы формы
    const registrationForm = document.getElementById('registration-form');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const passwordError = document.getElementById('password-error');
    const phoneInput = document.getElementById('phone');

    // Обработка отправки формы
    registrationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Очищаем предыдущие ошибки
        passwordError.textContent = '';
        
        // Проверка совпадения паролей
        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordError.textContent = 'Пароли не совпадают';
            return;
        }
        
        // Проверка сложности пароля
        if (passwordInput.value.length < 8) {
            passwordError.textContent = 'Пароль должен содержать не менее 8 символов';
            return;
        }
        
        // Получаем значения полей
        const fullname = document.getElementById('fullname').value;
        const phone = phoneInput.value;
        const email = document.getElementById('email').value;
        const password = passwordInput.value;
        const license = document.getElementById('license').value;
        
        // Проверяем, существует ли уже такой пользователь
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const existingUser = users.find(user => user.email === email);
        
        if (existingUser) {
            passwordError.textContent = 'Пользователь с таким email уже зарегистрирован';
            return;
        }
        
        // Создаем нового пользователя
        const newUser = {
            fullname,
            phone,
            email,
            password, // В реальном приложении пароль должен быть захеширован
            license,
            registrationDate: new Date().toISOString()
        };
        
        // Добавляем пользователя в хранилище
        users.push(newUser);
        localStorage.setItem('users', JSON.stringify(users));
        
        // Выводим сообщение об успешной регистрации и перенаправляем
        alert('Регистрация успешна! Теперь вы можете войти в систему.');
        window.location.href = 'login.html';
    });
    
    // Форматирование номера телефона при вводе
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
});