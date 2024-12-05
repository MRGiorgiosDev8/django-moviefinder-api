document.addEventListener('DOMContentLoaded', function () {
    const signupLink = document.getElementById('signup-link');
    const loginLink = document.getElementById('login-link');
    const signupLine = signupLink.querySelector('.nav-line');
    const loginLine = loginLink.querySelector('.nav-line');

    function getLineWidth(line) {
        const computedStyle = window.getComputedStyle(line);
        return computedStyle.getPropertyValue('--line-width');
    }

    signupLink.addEventListener('mouseenter', () => {
        const lineWidth = getLineWidth(signupLine);
        gsap.to(signupLine, {
            duration: 0.1,
            width: lineWidth,
            ease: "power4.out"
        });
    });

    signupLink.addEventListener('mouseleave', () => {
        gsap.to(signupLine, {
            duration: 0.1,
            width: '0%',
            ease: "power4.out"
        });
    });

    loginLink.addEventListener('mouseenter', () => {
        const lineWidth = getLineWidth(loginLine);
        gsap.to(loginLine, {
            duration: 0.1,
            width: lineWidth,
            ease: "power4.out"
        });
    });

    loginLink.addEventListener('mouseleave', () => {
        gsap.to(loginLine, {
            duration: 0.1,
            width: '0%',
            ease: "power4.out"
        });
    });
});