document.addEventListener('DOMContentLoaded', function() {
    // Проверка авторизации
    if (typeof window.checkAuth === 'function') {
        window.checkAuth();
    } else {
        // Если функция не определена, реализуем свою проверку
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        if (!isLoggedIn) {
            window.location.href = 'login.html';
            return;
        }
    }
    
    // Получаем элементы
    const requestForm = document.getElementById('request-form');
    const itemSelect = document.getElementById('item');
    const dateInput = document.getElementById('date');
    const selectedItemInfo = document.getElementById('selected-item-info');
    const itemDetails = document.getElementById('item-details');
    
    // Проверяем наличие элементов на странице
    if (!requestForm || !itemSelect) {
        console.error('Критические элементы формы не найдены');
        return;
    }
    
    // Устанавливаем минимальную дату (сегодня)
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    dateInput.min = formattedDate;
    
    // Загрузка данных товаров
    loadItems();
    
    // Обработчик выбора товара
    itemSelect.addEventListener('change', function() {
        const selectedItemId = this.value;
        
        if (selectedItemId && selectedItemInfo && itemDetails) {
            // Показываем информацию о выбранном товаре
            showItemDetails(selectedItemId);
        } else if (selectedItemInfo) {
            // Скрываем информацию, если товар не выбран
            selectedItemInfo.style.display = 'none';
        }
    });
    
    // Обработчик отправки формы
    requestForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Получаем значения полей
        const itemId = itemSelect.value;
        const date = dateInput.value;
        const comment = document.getElementById('comment')?.value || '';
        
        // Проверка полей
        if (!itemId || !date) {
            alert('Пожалуйста, выберите товар и дату');
            return;
        }
        
        // Получаем данные выбранного товара
        const selectedOption = itemSelect.querySelector(`option[value="${itemId}"]`);
        if (!selectedOption) {
            alert('Ошибка при получении данных товара');
            return;
        }
        
        let itemData;
        try {
            itemData = JSON.parse(selectedOption.dataset.item);
        } catch (error) {
            console.error('Ошибка при парсинге данных товара:', error);
            itemData = {
                name: selectedOption.textContent.split(' - ')[0],
                price: parseInt(selectedOption.textContent.split(' - ')[1]) || 0
            };
        }
        
        // Получаем данные пользователя
        const userEmail = localStorage.getItem('userEmail') || '';
        const userName = localStorage.getItem('userName') || 'Пользователь';
        
        // Формируем дату в формате дд.мм.гггг
        const requestDate = new Date(date);
        const formattedRequestDate = requestDate.toLocaleDateString('ru-RU');
        
        // Получаем существующие заявки
        const allRequests = JSON.parse(localStorage.getItem('itemRequests') || '[]');
        
        // Создаем новую заявку
        const newRequestId = allRequests.length > 0 ? Math.max(...allRequests.map(req => req.id)) + 1 : 1;
        
        const newRequest = {
            id: newRequestId,
            itemId: itemId,
            item: itemData.name,
            date: formattedRequestDate,
            comment: comment,
            userEmail: userEmail,
            userName: userName,
            phone: localStorage.getItem('userPhone') || '+7 (XXX) XXX-XX-XX',
            status: 'new',
            createdAt: new Date().toISOString()
        };
        
        // Добавляем заявку в список
        allRequests.push(newRequest);
        
        // Сохраняем обновленный список
        localStorage.setItem('itemRequests', JSON.stringify(allRequests));
        
        // Показываем сообщение об успехе
        alert('Заявка успешно отправлена!');
        
        // Перенаправляем на страницу заявок
        window.location.href = 'requests.html';
    });
    
    // Функция загрузки списка товаров
    function loadItems() {
        // Для демонстрации используем моковые данные
        const mockItems = [
            {
                id: 1,
                name: 'Товар 1',
                price: 5000,
                attribute1: 'Значение 1',
                attribute2: 'Значение 2',
                description: 'Подробное описание товара 1'
            },
            {
                id: 2,
                name: 'Товар 2',
                price: 5500,
                attribute1: 'Значение 1',
                attribute2: 'Значение 2',
                description: 'Подробное описание товара 2'
            },
            {
                id: 3,
                name: 'Товар 3',
                price: 5200,
                attribute1: 'Значение 1',
                attribute2: 'Значение 2',
                description: 'Подробное описание товара 3'
            },
            {
                id: 4,
                name: 'Товар 4',
                price: 3800,
                attribute1: 'Значение 1',
                attribute2: 'Значение 2',
                description: 'Подробное описание товара 4'
            },
            {
                id: 5,
                name: 'Товар 5',
                price: 4200,
                attribute1: 'Значение 1',
                attribute2: 'Значение 2',
                description: 'Подробное описание товара 5'
            }
        ];
        
        populateItemSelect(mockItems);
    }
    
    // Функция заполнения выпадающего списка товаров
    function populateItemSelect(items) {
        // Очищаем текущий список, сохраняя первый элемент (опцию "Выберите товар")
        itemSelect.innerHTML = '<option value="">-- Выберите товар --</option>';
        
        // Добавляем товары в список
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = `${item.name} - ${item.price} ₽/день`;
            option.dataset.item = JSON.stringify(item); // Сохраняем данные товара для быстрого доступа
            itemSelect.appendChild(option);
        });
    }
    
    // Функция отображения информации о выбранном товаре
    function showItemDetails(itemId) {
        // Находим выбранный элемент списка
        const selectedOption = itemSelect.querySelector(`option[value="${itemId}"]`);
        
        if (!selectedOption) return;
        
        // Получаем данные товара
        try {
            const item = JSON.parse(selectedOption.dataset.item);
            
            // Заполняем блок с информацией
            itemDetails.innerHTML = `
                <div class="item-card">
                    <img src="https://via.placeholder.com/400x250" alt="${item.name}" class="item-img">
                    <div class="item-details">
                        <h3 class="item-title">${item.name}</h3>
                        <p class="item-info"><strong>Характеристика 1:</strong> ${item.attribute1}</p>
                        <p class="item-info"><strong>Характеристика 2:</strong> ${item.attribute2}</p>
                        <p class="item-info"><strong>Стоимость:</strong> ${item.price} ₽/день</p>
                        <p class="item-description">${item.description}</p>
                    </div>
                </div>
            `;
            
            // Показываем блок с информацией
            selectedItemInfo.style.display = 'block';
        } catch (error) {
            console.error('Ошибка при получении данных товара:', error);
        }
    }
});