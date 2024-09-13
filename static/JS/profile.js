document.getElementById('edit-btn').addEventListener('click', function() {
    document.querySelectorAll('.profile-detail-item span:nth-child(2)').forEach(span => {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = span.textContent;
        span.parentNode.replaceChild(input, span);
    });
    document.getElementById('edit-btn').style.display = 'none';
    document.getElementById('save-btn').style.display = 'block';
});

document.getElementById('save-btn').addEventListener('click', function() {
    document.querySelectorAll('.profile-detail-item input').forEach(input => {
        const span = document.createElement('span');
        span.textContent = input.value;
        input.parentNode.replaceChild(span, input);
    });
    document.getElementById('edit-btn').style.display = 'block';
    document.getElementById('save-btn').style.display = 'none';
});
