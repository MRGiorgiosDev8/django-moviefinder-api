document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    const heading = document.getElementById("auth-h2");

    if (form) {
        gsap.set(form, {
            clipPath: "inset(100% 0 50% 0)",
            opacity: 0,
        });

        gsap.to(form, {
            clipPath: "inset(0% 0 0% 0)",
            opacity: 1,
            duration: 0.6,
            ease: "power2.out",
        });
    }

    if (heading) {
        gsap.fromTo(
            heading,
            { y: 40, opacity: 0 },
            {
                y: 0,
                opacity: 1,
                duration: 1,
                ease: "back.out(1.7)",
                delay: 0.3,
            }
        );
    }
});