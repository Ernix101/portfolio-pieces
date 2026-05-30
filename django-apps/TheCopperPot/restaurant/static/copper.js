window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 90) {
        nav.style.background = 'rgba(12, 6, 2, 0.8)';
    } else {
        nav.style.background = 'transparent';
    }
});

// ! Making sure the navigation appears on pages without the hero image
const hero = document.querySelector('.hero');
if(!hero){
    document.querySelector('nav').classList.add('solid');
}

//* changing the nav bar to hamburger when clicked
document.getElementById('hamburger').addEventListener('click', () => {
    document.getElementById('nav-menu').classList.toggle('open');
});
