const hideBlock2 = document.querySelectorAll('.hide-block');
/*const modalWnd = document.querySelectorAll('.modal-w');
const modalOpenBtns = document.querySelectorAll('.add-cart');
const extBtn = document.getElementById('ext-btn');
const modalName = document.querySelector('.name-inp');
const modalPrice = document.querySelector('.price-inp');
const modalSKU = document.getElementById('sku-inp');*/
const allModals2 = document.querySelectorAll('.modal-block');
//const dots2 = document.querySelectorAll('.dot');
//const slides2 = document.querySelectorAll('.slide');







function quite2() {
    for (let modal of allModals2) {
        modal.classList.remove('active')
    }
}






for (let hide of hideBlock2) {
    hide.onclick = (e) => {
        if (e.target.classList.contains('hide-block')) {
            quite2()
        }
    }
}




const cartOpen = document.getElementById('cart-btn');
const cartBlock = document.querySelector('.cart-block');
const cartClose = document.getElementById('cart-close-btn')

cartOpen.onclick = () => {
    hideBlock2[0].classList.add('active')
    cartBlock.classList.add('active')
}


cartClose.onclick = () => {
    quite2()
    cartBlock.classList.remove('active')
}


const openLnkBlock = document.getElementById('open-links-block');
const linksBlock = document.getElementById('links-block');
const linkBlkExt = document.querySelector('.exit-links-block');

openLnkBlock.onclick = () => {
    linksBlock.classList.add('active');
    hideBlock2[0].classList.add('active');
}


linkBlkExt.onclick = () => {
    quite2()
}





