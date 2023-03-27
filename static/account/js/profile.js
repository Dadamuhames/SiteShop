const sbmBtn = document.querySelector('.hide-sbmt');
const abtInp = document.querySelector('.abt-txt');


if(abtInp) {
    abtInp.oninput = () => {
        sbmBtn.classList.add('active')
    }
}

const pages = document.querySelectorAll('.pages');
const pgLinks = document.querySelectorAll('.page-li');


int = Number(JSON.parse(localStorage.getItem('i')))
pages[int].classList.add('active')
pgLinks[int].classList.add('active')



const openPage = (j) => {
    for (let l = 0; l < pages.length; l++) {
        pages[l].classList.remove('active')
        pgLinks[l].classList.remove('active')
    }
    pgLinks[j].classList.add('active');
    pages[j].classList.add('active')
    localStorage.setItem('i', JSON.stringify(j))
}


pgLinks.forEach((el, i) => {
    el.onclick = () => {
        openPage(i)
    }
})


const logoutBtn = document.getElementById('lg-btn');
const logoutBlock = document.getElementById('lg-block');

logoutBtn.onclick = () => {
    logoutBlock.classList.toggle('active')
}


const lnkBtn = document.querySelector('.change-prof');

lnkBtn.onclick = () => {
    openPage(5)
}


$('#modal-img').on('click', function() {
    $('.hidden-black-modal').addClass('active')
})


$('.exit-btns').on('click', function () {
    $('.hidden-black-modal').removeClass('active')
})


$('.profile-img-inp').on("input", function(e) {
    $('.profile-image-block').addClass("active")
    let val = $(e.target.files)[0]
    var reader = new FileReader();
    reader.onload = ((e) => {
        $('#profile-img').attr('src', e.target.result)
    });
    reader.readAsDataURL(val);
})