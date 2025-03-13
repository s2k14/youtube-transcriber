document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('transcribeForm');
    const submitBtn = document.getElementById('submitBtn');
    const submitBtnText = document.getElementById('submitBtnText');
    const submitSpinner = document.getElementById('submitSpinner');
    const errorAlert = document.getElementById('errorAlert');
    const results = document.getElementById('results');
    const transcriptDiv = document.getElementById('transcript');
    const summaryDiv = document.getElementById('summary');
    const downloadBtn = document.getElementById('downloadBtn');

    // Video info elements
    const videoThumbnail = document.getElementById('videoThumbnail');
    const videoTitle = document.getElementById('videoTitle');
    const videoDuration = document.getElementById('videoDuration');

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

    function formatDuration(duration) {
        // Convert ISO 8601 duration to readable format
        const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
        const hours = (match[1] || '').replace('H', '');
        const minutes = (match[2] || '').replace('M', '');
        const seconds = (match[3] || '').replace('S', '');

        let parts = [];
        if (hours) parts.push(`${hours}h`);
        if (minutes) parts.push(`${minutes}m`);
        if (seconds) parts.push(`${seconds}s`);

        return parts.join(' ') || '0s';
    }

    downloadBtn.addEventListener('click', async function() {
        try {
            const formData = new FormData();
            formData.append('transcript', transcriptDiv.textContent);

            const response = await fetch('/download-transcript', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to download transcript');
            }

            // Create a blob from the response and trigger download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'transcript.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            showError(error.message);
        }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        hideError();
        results.classList.add('d-none');
        downloadBtn.disabled = true;
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

            // Update video information
            videoThumbnail.src = data.video_info.thumbnail;
            videoTitle.textContent = data.video_info.title;
            videoDuration.textContent = `Duration: ${formatDuration(data.video_info.duration)}`;

            // Show results
            transcriptDiv.textContent = data.transcript;
            summaryDiv.textContent = data.summary;
            results.classList.remove('d-none');
            downloadBtn.disabled = false;

        } catch (error) {
            showError(error.message);
        } finally {
            showLoading(false);
        }
    });
});