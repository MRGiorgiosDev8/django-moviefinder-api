document.addEventListener('DOMContentLoaded', () => {
    const stickySelectors = ['.profile-card', '.edit-profile-card'];
    const container = document.querySelector('.container');
    const offsetTop = 11 * window.innerHeight / 100;

    if (window.innerWidth > 768) {
        stickySelectors.forEach((selector) => {
            const stickyElement = document.querySelector(selector);

            if (stickyElement) {
                const observer = new IntersectionObserver(
                    ([entry]) => {
                        if (entry.boundingClientRect.top < offsetTop) {
                            stickyElement.style.position = 'fixed';
                            stickyElement.style.top = `${offsetTop}px`;
                        } else {
                            stickyElement.style.position = 'static';
                        }
                    },
                    {
                        root: null,
                        threshold: 0,
                    }
                );

                observer.observe(container);
            }
        });
    }
});