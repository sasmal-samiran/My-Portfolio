// preloading page
window.addEventListener("load", () => {
    const loader = document.getElementById("loader-wrapper");
    loader.style.display = "none";
    const mainWebsite = document.getElementById("main-website");
    mainWebsite.style.display = "block";
});

////// menu button and toggle popup menu
const mediaQueryWidth1100 = window.matchMedia('(max-width: 1100px)');
const menuButton = document.querySelector('.menu-button');
const popupMenu = document.querySelector('.right-navbar');
const menuIcon = document.querySelector('.menu-icon');

function handleMobileMenu(e) {
    if (e.matches) {
        // Enable mobile menu behavior
        menuButton.addEventListener('click', toggleMenu);
        document.addEventListener('click', closeMenuOnOutsideClick);
        popupMenu.style.display = 'none';

        popupMenu.addEventListener('mouseenter', addMenuHoverEffect);
        popupMenu.addEventListener('mouseleave', removeMenuHoverEffect);
    } else {
        // Reset to desktop state
        menuButton.removeEventListener('click', toggleMenu);
        document.removeEventListener('click', closeMenuOnOutsideClick);
        popupMenu.removeEventListener('mouseenter', addMenuHoverEffect);
        popupMenu.removeEventListener('mouseleave', removeMenuHoverEffect);

        popupMenu.classList.remove('right-navbar-active');
        menuIcon.classList.remove('fa-xmark');

        popupMenu.style.display = '';
        popupMenu.classList.remove('mobile-popup');
    }
}

mediaQueryWidth1100.addEventListener('change', handleMobileMenu);
handleMobileMenu(mediaQueryWidth1100);

// Menu toggle
function toggleMenu(e) {
    e.stopPropagation();

    const isActive = popupMenu.classList.toggle('right-navbar-active');
    menuIcon.classList.toggle('fa-xmark');

    if (isActive) {
        popupMenu.classList.add('mobile-popup');
        popupMenu.style.display = 'flex';
    } else {
        popupMenu.style.display = 'none';
    }
}

// Outside click closes menu
function closeMenuOnOutsideClick(e) {
    if (!popupMenu.contains(e.target) && !menuButton.contains(e.target)) {
        popupMenu.style.display = 'none';
        popupMenu.classList.remove('right-navbar-active');
        popupMenu.classList.remove('mobile-popup');
        menuIcon.classList.remove('fa-xmark');
    }
}

// Hover effects (desktop only)
function addMenuHoverEffect() {
    popupMenu.classList.add('hover-effect');
}

function removeMenuHoverEffect() {
    popupMenu.classList.remove('hover-effect');
}

// navbar button animation
const navButtons = document.querySelectorAll('.nav-button');
const navSections = document.querySelectorAll('.nav-section');
window.addEventListener('scroll', () => {
    navSections.forEach((navSection, index) => {
        const sectionTop = navSection.offsetTop;
        const sectionHeight = navSection.offsetHeight;
        const scrollPosition = window.pageYOffset;
        if (scrollPosition <= 400) {
            navButtons.forEach(btn => btn.classList.remove('special-color'));
            navButtons[0].classList.add('special-color');
        }
        else if (scrollPosition >= sectionTop - sectionHeight / 3 &&
            scrollPosition < sectionTop + sectionHeight - sectionHeight / 3) {
            navButtons.forEach(btn => btn.classList.remove('special-color'));
            navButtons[index].classList.add('special-color');
        }
    });
});
// -----------------------------------------

// profile pic handling
const profilePic = document.querySelector('.profile-pic');
const leftNavbar = document.querySelector('.left-navbar');
let mediaQueryHeight600 = window.matchMedia('(max-height: 588px)');
let mediaQueryWidth10 = window.matchMedia('(max-width: 10px)');

function moveProfilePic() {
    profilePic.style.top = '46px';
    profilePic.style.left = '50px';
    profilePic.style.transform = 'translate(-50%, -50%) scale(0.16)';
    leftNavbar.style.marginLeft = '60px';
}
function resetProfilePic() {
    profilePic.style.top = '50%';
    profilePic.style.left = '50%';
    profilePic.style.transform = 'translate(-50%, -50%) scale(1)';
    leftNavbar.style.marginLeft = '35px';
}
window.addEventListener('resize', function () {
    if (mediaQueryHeight600.matches) {
        moveProfilePic();
    } else if (window.scrollY <= 30) {
        resetProfilePic();
    }
});

window.addEventListener('scroll', function () {
    if (window.scrollY >= 30 || mediaQueryHeight600.matches) {
        moveProfilePic();
    } else {
        resetProfilePic();
    }
});
// navbar handling with scroll up button animation
const topNavbar = document.querySelector('.top-navbar');
const scrollUp = document.querySelector('.scroll-up');
window.addEventListener('scroll', () => {
    if (window.pageYOffset >= 400) {
        topNavbar.style.background = 'rgb( 0,0,0,0.6)';
        scrollUp.style.opacity = '1';
    } else {
        topNavbar.style.background = 'transparent';
        scrollUp.style.opacity = '0';
    }
});

// -----------------------------------------

// about section
// about description animation
const innerAboutPic = document.querySelector('.inner-about-pic');
const innerAboutPicImg = document.querySelector('.inner-about-pic-img');
const aboutPicButton = document.querySelector('.about-pic-button');

function animateAboutPic(e) {
    e.stopPropagation();
    innerAboutPic.style.background = 'linear-gradient(65deg, #00ffff, #33ffcc, #00ff99)';
    innerAboutPic.style.boxShadow = '#00ffff -20px 20px 40px';
    innerAboutPic.style.transformOrigin = 'bottom';
    innerAboutPic.style.width = '330px';
    innerAboutPic.style.transform = 'rotateX(50deg)';
    innerAboutPicImg.style.transform = 'translateY(-50px) translateX(10px) scale(1.2)';
}
function removeAboutAnimation() {
    innerAboutPic.style.background = 'linear-gradient(65deg, #00ff99, #33ffcc, #00ffff)';
    innerAboutPic.style.boxShadow = '#00ff99 -10px 10px 30px';
    innerAboutPic.style.width = '300px';
    innerAboutPic.style.transform = 'none';
    innerAboutPicImg.style.transform = 'scale(1)';
}

innerAboutPicImg.addEventListener('mouseenter', animateAboutPic);
innerAboutPicImg.addEventListener('mouseleave', removeAboutAnimation);
aboutPicButton.addEventListener('click', (e) => {
    animateAboutPic(e);
    setTimeout(() => {
        removeAboutAnimation();
        aboutPicButton.innerHTML = 'Click Again';
    }, 3000);
});

// top description button handling
const hiddenDescription = document.querySelector('.hidden-description');
const hiddenDescriptionOnButton = document.querySelector('.hidden-description-on');
const hiddenDescriptionOffButton = document.querySelector('.hidden-description-off');

hiddenDescriptionOnButton.addEventListener('click', () => {
    hiddenDescription.style.display = 'block';
    hiddenDescriptionOnButton.style.display = 'none';
    logWidth();
});
hiddenDescriptionOffButton.addEventListener('click', () => {
    hiddenDescription.style.display = 'none';
    hiddenDescriptionOnButton.style.display = 'block';
    logWidth();
});

// ////// project cards handling
const projectCardImage = document.querySelectorAll('.project-card-image');
const magnifyPage = document.querySelector('.magnify-page');
const magnify = document.querySelectorAll('.magnify');
const magnifyImage = document.querySelector('.magnify-image');
const closeImage = document.querySelector('.close-image');

magnify.forEach((element, index) => {
    element.addEventListener('click', () => {
        magnifyPage.style.display = 'flex';
        magnifyImage.style.backgroundImage = `url(${projectCardImage[index].getAttribute('src')})`;
    });
});

closeImage.addEventListener('click', () => {
    magnifyImage.style.backgroundImage = '';
    magnifyPage.style.display = 'none';
});

// mobile message animation
function post() {
    send.classList.add('small');
    setTimeout(() => {
        send.classList.remove('small');
    }, 400);
}
const messages = document.querySelectorAll('.messages');
const send = document.querySelector('.text-send');
function mobileAnimation() {
    setTimeout(() => {
        post();
        messages[0].style.opacity = '1';
    }, 2520);
    setTimeout(() => {
        post();
        messages[1].style.opacity = '1';
        messages[0].classList.add('bubble-1');
    }, 5040);
    setTimeout(() => {
        post();
        messages[2].style.opacity = '1';
        messages[0].classList.add('bubble-2');
        messages[0].classList.remove('bubble-1');
        messages[1].classList.add('bubble-1');
    }, 7680);
    setTimeout(() => {
        post();
        messages[3].style.opacity = '1';
        messages[0].classList.add('bubble-3');
        messages[0].classList.remove('bubble-2');
        messages[1].classList.add('bubble-2');
        messages[1].classList.remove('bubble-1');
        messages[2].classList.add('bubble-1');
    }, 10000);
    setTimeout(() => {
        messages.forEach(message => {
            message.style.opacity = '0';
            message.classList.remove('bubble-1', 'bubble-2', 'bubble-3');
        });
        mobileAnimation();
    }, 13000);
}

async function type(string) {
    return new Promise(resolve => {
        const typed = new Typed('#text-message', {
            strings: [string],
            typeSpeed: 40,
            cursorChar: '',
            loop: false,
            onComplete: () => {
                typed.destroy();
                resolve();
            }
        });
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function startType() {
    const strings = [
        "Hi, I am Samiran Sasmal",
        "Open to invent with you",
        "Let's build smart together",
        "Code, Learn, Share"
    ];

    while (true) {
        for (const str of strings) {
            await sleep(1000);
            await type(str);
        }
        await sleep(3000);
    }
}

// contact details animation
const contactDetails = document.querySelector('.contact-details');
const contactElements = document.querySelectorAll('.contact-element');
const contactShadow = document.querySelector('.contact-shadow');

function contactAnimation() {
    contactDetails.classList.add('fly');
    contactShadow.classList.add('visible');

    let idx = 0;
    let count = 0;
    const intervalId = setInterval(() => {
        contactElements.forEach(el => el.classList.remove('flow'));
        contactElements[idx].classList.add('flow');

        idx = (idx + 1) % contactElements.length;
        count++;

        if (count >= contactElements.length) {
            clearInterval(intervalId);
            setTimeout(() => {
                contactDetails.classList.remove('fly');
                contactShadow.classList.remove('visible');
                contactElements.forEach(el => el.classList.remove('flow'));
            }, 1000);
        }
    }, 1000);
}


const animateScreen = document.querySelectorAll(".message-panel, .contact-details");

const animateScreenObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const el = entry.target;

            if (el.classList.contains("message-panel")) {
                mobileAnimation();
                startType();
                messages.forEach(message => {
                    message.style.opacity = '0';
                });
            }

            if (el.classList.contains("contact-details")) {
                contactAnimation();
                setInterval(() => {
                    contactAnimation();
                }, 10000);
            }

            observer.unobserve(el);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: "0px 0px 100px 0px"
});

animateScreen.forEach(el => animateScreenObserver.observe(el));
