document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('ttsForm');
    const submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
        // Validasi teks
        const textInput = document.getElementById('textInput');
        if (textInput.value.trim() === '') {
            e.preventDefault();
            alert('Silakan masukkan teks terlebih dahulu!');
            textInput.focus();
            return;
        }

        // Tampilkan loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-circle-notch loading me-2"></i> Memproses...';

        // Set timeout untuk memastikan button kembali normal jika ada error
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i> Generate & Download Suara';
        }, 10000);
    });

    // Fitur hitung karakter
    const textArea = document.getElementById('textInput');
    const charCounter = document.createElement('div');
    charCounter.className = 'text-end text-muted small mt-1';
    textArea.parentNode.insertBefore(charCounter, textArea.nextSibling);

    textArea.addEventListener('input', function () {
        const currentLength = this.value.length;
        charCounter.textContent = `${currentLength}/200 karakter`;

        if (currentLength > 200) {
            charCounter.classList.add('text-danger');
        } else {
            charCounter.classList.remove('text-danger');
        }
    });

    // Set nilai awal slider kecepatan
    const speedRange = document.getElementById('speedRange');
    const speedValue = document.getElementById('speedValue');
    if (speedRange && speedValue) {
        speedValue.innerText = speedRange.value;
        speedRange.addEventListener('input', function () {
            speedValue.innerText = this.value;
        });
    }
});