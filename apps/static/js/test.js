document.addEventListener('DOMContentLoaded', function() {
    const headers = document.querySelectorAll('.collapsible-header');

    headers.forEach(header => {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
        });
    });
});
