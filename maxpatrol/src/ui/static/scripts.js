function showLoading() {
    document.getElementById('loading').style.display = 'block';
    var progressBar = document.querySelector('.progress-bar');
    progressBar.style.width = '0%';

    // Пример, чтобы показать, как прогресс будет обновляться
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            progressBar.style.width = width + '%';
        }
    }, 10); // Изменяйте скорость обновления здесь
}
