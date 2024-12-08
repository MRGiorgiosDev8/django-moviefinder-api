document.addEventListener('DOMContentLoaded', function () {
    const profileLink = document.getElementById('profile-link');
    const logoutLink = document.getElementById('logout-link');
    const signupLink = document.getElementById('signup-link');
    const loginLink = document.getElementById('login-link');
    const profileLine = profileLink ? profileLink.querySelector('.nav-line') : null;
    const logoutLine = logoutLink ? logoutLink.querySelector('.nav-line') : null;
    const signupLine = signupLink ? signupLink.querySelector('.nav-line') : null;
    const loginLine = loginLink ? loginLink.querySelector('.nav-line') : null;

    function getLineWidth(line) {
        const computedStyle = window.getComputedStyle(line);
        return computedStyle.getPropertyValue('--line-width');
    }

    if (profileLink && profileLine) {
        profileLink.addEventListener('mouseenter', () => {
            const lineWidth = getLineWidth(profileLine);
            gsap.to(profileLine, {
                duration: 0.1,
                width: lineWidth,
                ease: "power4.out"
            });
        });

        profileLink.addEventListener('mouseleave', () => {
            gsap.to(profileLine, {
                duration: 0.1,
                width: '0%',
                ease: "power4.out"
            });
        });
    }

    if (logoutLink && logoutLine) {
        logoutLink.addEventListener('mouseenter', () => {
            const lineWidth = getLineWidth(logoutLine);
            gsap.to(logoutLine, {
                duration: 0.1,
                width: lineWidth,
                ease: "power4.out"
            });
        });

        logoutLink.addEventListener('mouseleave', () => {
            gsap.to(logoutLine, {
                duration: 0.1,
                width: '0%',
                ease: "power4.out"
            });
        });
    }

    if (signupLink && signupLine) {
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
    }

    if (loginLink && loginLine) {
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
    }
});