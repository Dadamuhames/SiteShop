const pages2 = document.querySelectorAll('.pages');
const pgLinks2 = document.querySelectorAll('.page-li');


pgLinks2.forEach((el, i) => {
    el.onclick = () => {
        for (let l = 0; l < pages2.length; l++) {
            pages2[l].classList.remove('active')
            pgLinks2[l].classList.remove('active')
        }
        pgLinks2[i].classList.add('active');
        pages2[i].classList.add('active')
    }
})
