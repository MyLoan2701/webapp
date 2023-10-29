window.onload = function() {


    // =================== web 2 tìm nâng cao ================
    // Thêm hình vào banner
    setupBanner();


    // Thêm danh sách hãng điện tho// ==================== End ===========================

};

function setupBanner() {

            // Khởi động thư viện hỗ trợ banner - chỉ chạy khi đã tạo hình trong banner
            $('.owl-carousel').owlCarousel({
                items: 1.5,
                margin: 100,
                center: true,
                loop: true,
                smartSpeed: 450,
                nav: false,

                autoplay: true,
                autoplayTimeout: 3500,

                responsive: {
                    0: {
                        items: 1
                    },
                    600: {
                        items: 1.25
                    },
                    1000: {
                        items: 1.5
                    }
                }
            });


    
}

function addBanner(img, link) {
    // <a target='_blank' href=` + link + `>
    var newDiv = `<div class='item'>
                        <img src=` + img + `>
                    </div>`;
    var banner = document.getElementsByClassName('owl-carousel')[0];
    banner.innerHTML += newDiv;
}

function addSmallBanner(img) {
    var newimg = `<img src=` + img + ` style="width: 100%;">`;
    var smallbanner = document.getElementsByClassName('smallbanner')[0];
    smallbanner.innerHTML += newimg;
}