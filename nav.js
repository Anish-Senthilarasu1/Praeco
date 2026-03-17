document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.category-btn');
    const activeIndicator = document.getElementById('active-indicator');
    let currentActiveButton = document.querySelector('.category-btn.active') || buttons[0];

    function updateActiveIndicator(button) {
        if (!button || !activeIndicator) return;
        const buttonRect = button.getBoundingClientRect();
        const containerRect = button.parentElement.getBoundingClientRect();
        activeIndicator.style.width = `${buttonRect.width}px`;
        activeIndicator.style.height = `${buttonRect.height}px`;
        activeIndicator.style.left = `${buttonRect.left - containerRect.left}px`;
        activeIndicator.style.top = `${buttonRect.top - containerRect.top}px`;
    }

    updateActiveIndicator(currentActiveButton);
    window.addEventListener('resize', () => updateActiveIndicator(currentActiveButton));

    buttons.forEach(button => {
        button.addEventListener('click', async function (e) {
            e.preventDefault();
            if (this === currentActiveButton) return;

            const page = this.getAttribute('data-page');

            // Update active state immediately
            currentActiveButton.classList.remove('active', 'font-semibold');
            this.classList.add('active', 'font-semibold');
            currentActiveButton = this;
            updateActiveIndicator(this);

            const grid = document.getElementById('articles-grid');

            // Fade out
            grid.style.transition = 'opacity 0.15s ease';
            grid.style.opacity = '0';

            try {
                const res = await fetch(page);
                const text = await res.text();
                const doc = new DOMParser().parseFromString(text, 'text/html');
                const newGrid = doc.getElementById('articles-grid');

                // Wait for fade out to finish
                await new Promise(r => setTimeout(r, 150));

                if (newGrid) {
                    grid.className = newGrid.className;
                    grid.innerHTML = newGrid.innerHTML;
                    history.pushState(null, '', page);
                } else {
                    window.location.href = page;
                    return;
                }
            } catch (err) {
                window.location.href = page;
                return;
            }

            // Fade in
            requestAnimationFrame(() => {
                grid.style.opacity = '1';
            });
        });
    });
});
