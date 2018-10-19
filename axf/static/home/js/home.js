$(document).ready(function () {
    setTimeout(function () {
        swiper1()
        swiper2()
    },1000)
});


function swiper1() {

    var mySwiper = new Swiper ('#topSwiper', {
        direction: 'horizontal',	//方向横向
        loop: true,
        
        autoplayDisableOnInteraction:false,
        autoplay : 2000,		//每秒轮播一次
        speed:2000,
        effect : 'coverflow',
        slidesPerView: 1,
        enteredSlides: true,
        coverflow: {
            rotate: 30,
            stretch: 10,
            depth: 60,
            modifier: 2,
            slideShadows : true
        }
    })
}


function swiper2() {
    var mySwiper2 = new Swiper('#swiperMenu', {
        slidesPerView : 3,
        // paginationClickable: true,
        // spaceBetween:2, //间距
        loop:false,
        effect : 'coverflow',
        centeredSlides: true,
        coverflow: {
            rotate: 90,
            stretch: 0,
            depth: 0,
            modifier: 0,
            slideShadows : true,
        },

    });

}

