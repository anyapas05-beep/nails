/**
 * LUMINIAL - ПОВНИЙ ТА СУВОРИЙ СКРИПТ ВАЛІДАЦІЇ
 */

// --- 1. ОБМЕЖЕННЯ ВВОДУ ---
window.setupInputRestrictions = function() {
    const firstName = document.querySelector('input[name="first_name"]');
    const lastName = document.querySelector('input[name="last_name"]');
    const phone = document.querySelector('input[name="phone"]');
    const alphaRegex = /[^a-zA-Zа-яА-ЯіІїЇєЄґҐ']/g;

    if (firstName) firstName.oninput = function() { this.value = this.value.replace(alphaRegex, ''); };
    if (lastName) lastName.oninput = function() { this.value = this.value.replace(alphaRegex, ''); };
    if (phone) phone.oninput = function() { this.value = this.value.replace(/[^0-9+]/g, ''); };
};

// --- 2. СУВОРА ВАЛІДАЦІЯ (Перевірка ТІЛЬКИ того, що бачить юзер) ---
window.validateStep = function(step) {
    const currentStep = document.getElementById('step-' + step);
    if (!currentStep) return true;

    // Отримуємо всі інпути всередині поточного кроку
    const inputs = currentStep.querySelectorAll('input, select');
    let isValid = true;

    inputs.forEach(input => {
        // Перевірка 1: Чи блок цього інпуту зараз видимий (не display: none)
        const isVisible = !!(input.offsetWidth || input.offsetHeight || input.getClientRects().length);

        // Перевірка 2: Чи це не квартира (квартира — єдине поле, яке може бути порожнім)
        const isOptional = input.placeholder && input.placeholder.toLowerCase().includes('кв.');

        if (isVisible && !isOptional) {
            if (!input.value.trim()) {
                input.style.borderBottom = "2px solid #ff5252"; // Робимо лінію червоною
                isValid = false;
            } else {
                input.style.borderBottom = "1px solid #ddd";
            }
        }
    });

    if (!isValid) {
        alert("Помилка! Заповніть усі дані для доставки (номер відділення або адресу)!");
    }
    return isValid;
};

// --- 3. НАВІГАЦІЯ ТА ПЕРЕМИКАННЯ КРОКІВ ---
window.goToStep = function(step) {
    // Якщо йдемо на крок 2 — спочатку валідуємо крок 1
    if (step === 2 && !window.validateStep(1)) return;

    const steps = document.querySelectorAll('.checkout-step');
    const nums = document.querySelectorAll('.step-num');

    steps.forEach(s => {
        s.style.display = 'none';
        s.classList.remove('active');
    });

    const target = document.getElementById('step-' + step);
    if (target) {
        target.style.display = 'block';
        target.classList.add('active');
    }
    nums.forEach((n, i) => n.classList.toggle('active', i + 1 === step));
};

// --- 4. ПЕРЕМИКАННЯ ДОСТАВКИ ---
window.toggleDeliveryFields = function() {
    const select = document.getElementById('delivery-select');
    if (!select) return;

    const method = select.value;
    const novaFields = document.getElementById('nova-poshta-fields');
    const ukrFields = document.getElementById('ukr-poshta-fields');

    if (novaFields && ukrFields) {
        novaFields.style.display = (method === 'nova') ? 'block' : 'none';
        ukrFields.style.display = (method === 'ukr') ? 'block' : 'none';
    }
};

// --- 5. ІНІЦІАЛІЗАЦІЯ ПРИ ЗАВАНТАЖЕННІ ---
document.addEventListener('DOMContentLoaded', function() {
    window.setupInputRestrictions();

    const deliverySelect = document.getElementById('delivery-select');
    if (deliverySelect) {
        deliverySelect.addEventListener('change', window.toggleDeliveryFields);
        window.toggleDeliveryFields();
    }

    // ГОЛОВНИЙ ФІКС: Блокуємо відправку форми, якщо валідація не пройшла
    const form = document.querySelector('form');
    if (form) {
        form.onsubmit = function(e) {
            if (!window.validateStep(2)) {
                e.preventDefault(); // Зупиняємо відправку!
                return false;
            }
            return true;
        };
    }
});
// Функція для показу деталей на сторінці "Доставка та Оплата"
window.showDetails = function(type) {
    const detailsBox = document.getElementById('delivery-info');
    const novaInfo = document.getElementById('nova-info');
    const ukrInfo = document.getElementById('ukr-info');

    if (detailsBox && novaInfo && ukrInfo) {
        detailsBox.classList.add('active'); // Додає клас для відображення (якщо є в CSS)
        detailsBox.style.display = 'block'; // Примусово показуємо блок

        novaInfo.style.display = (type === 'nova') ? 'block' : 'none';
        ukrInfo.style.display = (type === 'ukr') ? 'block' : 'none';

        // Плавний скрол до інформації
        detailsBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        console.error("Елементи delivery-info, nova-info або ukr-info не знайдені в HTML!");
    }
};