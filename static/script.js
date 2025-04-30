
////// window resizing events
function logWidth() {
    const videoHeight = document.querySelector('.background-video').offsetHeight;
    const footer = document.querySelector('.footer');
    const background = document.querySelector('.background-animation');
    background.style.top = videoHeight + 'px';
    background.style.height = footer.offsetTop - videoHeight + 'px';
}

window.addEventListener('resize', logWidth);
logWidth();

////// menu button and toggle popup menu
const mediaQueryWidth1100 = window.matchMedia('(max-width: 1100px)');
const menuButton = document.querySelector('.menu-button');
const popupMenu = document.querySelector('.right-navbar');
const menuIcon = document.querySelector('.menu-icon');

// media query handling 
function handleMobileMenu(mediaQueryWidth1100) {
    if (mediaQueryWidth1100.matches) {
        // Mobile screen behavior
        menuButton.addEventListener('click', toggleMenu);
        document.addEventListener('click', closeMenuOnOutsideClick);
        popupMenu.style.display = 'none';

        popupMenu.addEventListener('mouseenter', popupMouseenterEvent);
        popupMenu.addEventListener('mouseleave', popupMouseleaveEvent);
    } else {
        // Remove mobile behaviors if switching to desktop
        menuButton.removeEventListener('click', toggleMenu);
        document.removeEventListener('click', closeMenuOnOutsideClick);
        popupMenu.removeEventListener('mouseenter', popupMouseenterEvent);
        popupMenu.removeEventListener('mouseleave', popupMouseleaveEvent);
        popupMenu.classList.remove('right-navbar-active');
        menuIcon.classList.remove('fa-xmark');
        popupMenu.style.display = 'flex';
        popupMenu.style.position = 'static';
        popupMenu.style.backgroundColor = 'transparent';
        popupMenu.style.borderRadius = '0';
        popupMenu.style.width = 'auto';
        popupMenu.style.padding = '0';
        popupMenu.style.alignItems = 'center';
        popupMenu.style.flexDirection = 'row';
    }
}
handleMobileMenu(mediaQueryWidth1100);
mediaQueryWidth1100.addEventListener('change', handleMobileMenu);

function popupMouseenterEvent() {
    if (popupMenu) {
        const activeMenu = document.querySelector('.right-navbar-active');
        activeMenu.style.boxShadow = '0 0 10px rgba(255, 255, 255, 0.5)';
        activeMenu.style.transition = 'box-shadow 0.3s ease-in-out';
    }

}
function popupMouseleaveEvent() {
    const activeMenu = document.querySelector('.right-navbar-active');
    activeMenu.style.boxShadow = 'none';
}

function toggleMenu(e) {
    e.stopPropagation();
    menuIcon.classList.toggle('fa-xmark');
    popupMenu.classList.toggle('right-navbar-active');
    popupMenu.style.display = popupMenu.style.display === 'flex' ? 'none' : 'flex';
    popupMenu.style.position = 'absolute';
    popupMenu.style.backgroundColor = 'rgba(0,0,0,0.1)';
    popupMenu.style.backdropFilter = 'blur(10px)';
    popupMenu.style.top = '60px';
    popupMenu.style.right = '20px';
    popupMenu.style.borderRadius = '10px';
    popupMenu.style.flexDirection = 'column';
    popupMenu.style.width = '150px';
    popupMenu.style.padding = '20px 10px';
    popupMenu.style.alignItems = 'flex-start';
}

function closeMenuOnOutsideClick(e) {
    if (!popupMenu.contains(e.target) && !menuButton.contains(e.target)) {
        popupMenu.style.display = 'none';
        menuIcon.classList.remove('fa-xmark');
        popupMenu.classList.remove('right-navbar-active');
    }
}
// -----------------------------------------

// profile pic handling
const profilePic = document.querySelector('.profile-pic');
const leftNavbar = document.querySelector('.left-navbar');
let mediaQueryHeight600 = window.matchMedia('(max-height: 588px)');
let mediaQueryWidth10 = window.matchMedia('(max-width: 10px)');

function moveProfilePic(){
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
    if ( mediaQueryHeight600.matches) {
        moveProfilePic();
    }else if(window.scrollY <= 30) {
        resetProfilePic();
    }
});

window.addEventListener('scroll', function () {
    if (window.scrollY >= 30 || mediaQueryHeight600.matches) {
        moveProfilePic();
    }else {
        resetProfilePic();
    }
});
// navbar handling with scroll up button animation
const topNavbar = document.querySelector('.top-navbar');
const scrollUp = document.querySelector('.scroll-up');
window.addEventListener('scroll', () => {
    if(window.pageYOffset >= 400) {
        topNavbar.style.background = 'rgb( 0,0,0,0.6)';
        scrollUp.style.opacity = '1';
    }else {
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
innerAboutPicImg.addEventListener('mouseenter', animateAboutPic);
innerAboutPicImg.addEventListener('mouseleave', removeAboutAnimation);
aboutPicButton.addEventListener('click', (e) => {
    animateAboutPic(e);
    setTimeout( () => {
        removeAboutAnimation();
        aboutPicButton.innerHTML = 'Click Again';
    }, 3000);
});

function animateAboutPic(e) {
    e.stopPropagation();
    innerAboutPic.style.background = 'linear-gradient(65deg, #00ffff, #33ffcc, #00ff99)';
    innerAboutPic.style.boxShadow = '#00ffff -20px 20px 40px';
    innerAboutPic.style.transformOrigin = 'bottom';
    innerAboutPic.style.width = '330px';
    innerAboutPic.style.transform = 'rotateX(50deg)';
    innerAboutPicImg.style.transform = 'translateY(-50px) translateX(10px) scale(1.2)';
}
function removeAboutAnimation(){
    innerAboutPic.style.background = 'linear-gradient(65deg, #00ff99, #33ffcc, #00ffff)';
    innerAboutPic.style.boxShadow = '#00ff99 -10px 10px 30px';
    innerAboutPic.style.width = '300px';
    innerAboutPic.style.transform = 'none';
    innerAboutPicImg.style.transform = 'scale(1)';
}

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
})



