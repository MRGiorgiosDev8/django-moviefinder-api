const links = document.querySelectorAll('.btn-link-url');

links.forEach(link => {
    const arrow = link.querySelector('.arrow-icon');

    link.addEventListener('mouseenter', () => {
        gsap.killTweensOf(arrow);

        gsap.set(arrow, { display: 'inline-block', opacity: 0, x: 0 });
        gsap.to(arrow, { opacity: 1, duration: 0.3 });

        gsap.to(arrow, {
            x: 7,
            duration: 0.5,
            yoyo: true,
            repeat: -1,
            ease: "power1.inOut"
        });
    });

    link.addEventListener('mouseleave', () => {
        gsap.killTweensOf(arrow);

        gsap.to(arrow, {
            opacity: 0,
            duration: 0.3,
            onComplete: () => gsap.set(arrow, { display: 'none' })
        });
    });
});