const imgInputs = document.querySelector('.img-inp');
const slideings = document.querySelectorAll('.slide');
let imgDoots;
const imgSlidesprod = document.getElementById('prod-images');
let slideItems2 = [];
let imgDots2 = [];



function handleFiles(files) {
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var img = document.createElement("img");
        let imgdot = document.createElement("button");
        imgdot.classList.add('img-dot')
        if(i == 0) {
            imgdot.classList.add('active')
            img.classList.add("active");
        }
        btnimg = document.createElement("img");
        imgdot.appendChild(btnimg)
        img.classList.add("slide");
        img.file = file;
        imgSlidesprod.appendChild(img);
        imgDoots.appendChild(imgdot)
        var reader = new FileReader();
        reader.onload = (function (aImg, bimg) { return function (e) { aImg.src = e.target.result; bimg.src = e.target.result; }; })(img, btnimg);
        reader.readAsDataURL(file);
    }


}

imgInputs.addEventListener('change', (e) => {
    imgSlidesprod.innerHTML = '<div class="img-dots form-dots"></div>'
    imgDoots = document.querySelector('.img-dots')
    handleFiles(e.target.files)
    slideItems2 = document.querySelectorAll('.slide');
    imgDots2 = document.querySelectorAll('.img-dot');
    for (let i = 0; i < imgDots2.length; i++) {
        imgDots2[i].onclick = () => {
            for (let slide of slideItems2) {
                slide.classList.remove('active')
            }
            for (let dot of imgDots2) {
                dot.classList.remove('active')
            }
            slideItems2[i].classList.add('active')
            imgDots2[i].classList.add('active')
        }
    }
    
}, false)


for (let i = 0; i < imgDots2.length; i++) {
    imgDots2[i].onclick = () => {
        for (let slide of slideItems2) {
            slide.classList.remove('active')
        }
        for (let dot of imgDots2) {
            dot.classList.remove('active')
        }
        slideItems2[i].classList.add('active')
        imgDots2[i].classList.add('active')
    }
}



$('#id_category').change((e) => {
    let id = $(e.target).val()
    let url = '/get_categories/' + id

    $.ajax({
        url: url,
        type: 'GET',
        datatype: 'json',
        success: function (data) {
            $("#id_post_category").html(`<option value="">--- Post Category ---</option>`)
            for (let key in data) {
                $("#id_post_category").html($("#id_post_category").html() + `<option value="${data[String(key)]}">${key}</option>`)
            }
        }
    })
})

