/**
 * Функція для відображення деталей доставки
 * @param {string} type - Тип доставки ('nova' або 'ukr')
 */
function showDetails(type) {
    const detailsBox = document.getElementById('delivery-info');
    const novaInfo = document.getElementById('nova-info');
    const ukrInfo = document.getElementById('ukr-info');

    if (detailsBox && novaInfo && ukrInfo) {
        // Показуємо загальний контейнер
        detailsBox.classList.add('active');

        // Перемикаємо видимість конкретного блоку
        if (type === 'nova') {
            novaInfo.style.display = 'block';
            ukrInfo.style.display = 'none';
        } else if (type === 'ukr') {
            ukrInfo.style.display = 'block';
            novaInfo.style.display = 'none';
        }

        // Плавна прокрутка до інформації
        detailsBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Функція для приховування деталей доставки
 */
function hideDetails() {
    const detailsBox = document.getElementById('delivery-info');
    if (detailsBox) {
        detailsBox.classList.remove('active');
    }
}