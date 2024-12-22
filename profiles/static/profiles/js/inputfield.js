document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('#profile-update-form input, #profile-update-form select, #profile-update-form textarea');

    function updateInputStyle(input) {
        if (input.value.trim() !== '') {
            input.style.color = 'black';
        } else {
            input.style.color = 'grey';
        }
    }

    inputs.forEach(input => {
        updateInputStyle(input);

        input.addEventListener('input', () => updateInputStyle(input));
        input.addEventListener('change', () => updateInputStyle(input));
    });
});
