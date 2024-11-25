document.addEventListener("DOMContentLoaded", function () {
    gsap.registerPlugin(ScrollTrigger);

    gsap.set(".camera-movie, #movie-search-form", { opacity: 0, scale: 0 });

    ScrollTrigger.create({
        trigger: ".camera-movie",
        start: "top 80%",
        end: "top 20%",
        onEnter: () => {
            gsap.to(".camera-movie", {
                opacity: 1,
                scale: 1,
                duration: 0.8,
                ease: "power1.inOut",
            });
        },
        onLeaveBack: () => {
            gsap.to(".camera-movie", {
                opacity: 0,
                scale: 0,
                duration: 0.8,
                ease: "power1.inOut",
            });
        },
    });

    ScrollTrigger.create({
        trigger: "#movie-search-form",
        start: "top 80%",
        end: "top 20%",
        onEnter: () => {
            gsap.to("#movie-search-form", {
                opacity: 1,
                scale: 1,
                duration: 0.8,
                ease: "power1.inOut",
            });
        },
        onLeaveBack: () => {
            gsap.to("#movie-search-form", {
                opacity: 0,
                scale: 0,
                duration: 0.8,
                ease: "power1.inOut",
            });
        },
    });
});