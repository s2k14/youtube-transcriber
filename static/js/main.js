document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('transcribeForm');
    const submitBtn = document.getElementById('submitBtn');
    const submitBtnText = document.getElementById('submitBtnText');
    const submitSpinner = document.getElementById('submitSpinner');
    const errorAlert = document.getElementById('errorAlert');
    const results = document.getElementById('results');
    const transcriptDiv = document.getElementById('transcript');
    const summaryDiv = document.getElementById('summary');

    function showLoading(show) {
        submitBtn.disabled = show;
        submitBtnText.style.display = show ? 'none' : 'inline';
        submitSpinner.classList.toggle('d-none', !show);
    }

    function showError(message) {
        errorAlert.textContent = message;
        errorAlert.classList.remove('d-none');
    }

    function hideError() {
        errorAlert.classList.add('d-none');
        errorAlert.textContent = '';
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        hideError();
        results.classList.add('d-none');
        showLoading(true);

        try {
            const formData = new FormData(form);
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An unexpected error occurred');
            }

            // Show results
            transcriptDiv.textContent = data.transcript;
            summaryDiv.textContent = data.summary;
            results.classList.remove('d-none');

        } catch (error) {
            showError(error.message);
        } finally {
            showLoading(false);
        }
    });
});
