const loginFields = document.querySelectorAll('.login-field');

loginFields.forEach((loginField) => {
    const label = loginField.querySelector('.login-field-label');
    const input = loginField.querySelector('.login-field-input');

    const floatLabel = () => {
        label.style.top = '-10px';
    };

    const resetLabel = () => {
        if (!input.value && document.activeElement !== input) {
            label.style.top = '15px';
        }
    };

    loginField.addEventListener('mouseenter', floatLabel);
    loginField.addEventListener('mouseleave', resetLabel);

    input.addEventListener('focus', floatLabel);
    input.addEventListener('blur', resetLabel);
    input.addEventListener('click', floatLabel);
});