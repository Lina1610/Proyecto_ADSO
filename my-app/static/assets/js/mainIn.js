
// Initialize GSAP and TextPlugin (for animated text)
document.addEventListener("DOMContentLoaded", function () {
    gsap.registerPlugin(TextPlugin);
    gsap.set("#animated-text", { text: "", opacity: 0 });
    gsap.to("#animated-text", {
        duration: 2,
        opacity: 1,
        text: "TAMALES EL BUEN SAZÓN",
        ease: "power2.out",
        delay: 0.5
    });
});

// Handle menu scroll effect
window.addEventListener('scroll', function () {
    const menu = document.querySelector('.menu');
    let scrollPosition = window.scrollY;
    if (scrollPosition > 50) {
        menu.classList.add('scrolled');
    } else {
        menu.classList.remove('scrolled');
    }
});

// Initialize AOS (Animate on Scroll)
AOS.init({
    duration: 1000,
    once: false,
    easing: 'ease-in-out',
    mirror: true
});

// Handle WhatsApp button scroll behavior
document.addEventListener("DOMContentLoaded", function () {
    const whatsappBtn = document.querySelector('.whatsapp-btn');
    window.addEventListener('scroll', function () {
        const scrollPosition = window.scrollY;
        const viewportHeight = window.innerHeight;
        if (scrollPosition + viewportHeight > document.body.offsetHeight - 200) {
            whatsappBtn.style.bottom = '100px';
        } else {
            whatsappBtn.style.bottom = '40px';
        }
    });
});

// Initialize Accessibility (assuming this is from a library like sienna.js)
window.addEventListener('load', function () {
    new Accessibility();
}, false);