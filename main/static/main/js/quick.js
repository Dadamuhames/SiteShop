const sliderBlock = document.querySelector('.slider-items-img');
const blackFon = document.querySelector('.main-black');
let dots = document.querySelectorAll('.dot');
let slides = document.querySelectorAll('.slide');
sliderBlock.children[0].classList.add('active');
dots[0].classList.add('active')

function activeSLides(i) {
    for (let dot of dots) {
        dot.classList.remove('active')
    }
    for (let slide of slides) {
        slide.classList.remove('active')
    }
    dots[i].classList.add('active')
    slides[i].classList.add('active')
}

console.log(blackFon)
blackFon.onclick = () => {
    history.back()
    console.log(9)
}


for(let l = 0; l < dots.length; l++) {
    dots[l].onclick = () => {
        activeSLides(l)
    }
}