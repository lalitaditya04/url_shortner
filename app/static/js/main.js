function copyToClipboard() {
    const shortUrl = document.getElementById('short-url');
    shortUrl.select();
    shortUrl.setSelectionRange(0, 99999);
    document.execCommand('copy');

    // Show tooltip or alert
    alert('Copied to clipboard: ' + shortUrl.value);
}

// Initialize Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

