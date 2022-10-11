
    const slider = document.querySelector(".slider");
    const nextBtn = document.querySelector(".next-btn");
    const prevBtn = document.querySelector(".prev-btn");
    const slides = document.querySelectorAll(".slide");
    const slideIcons = document.querySelectorAll(".slide-icon");
    const numberOfSlides = slides.length;
    var slideNumber = 0;

    //image slider next button
    nextBtn.addEventListener("click", () => {
      slides.forEach((slide) => {
        slide.classList.remove("active");
      });
      slideIcons.forEach((slideIcon) => {
        slideIcon.classList.remove("active");
      });

      slideNumber++;

      if(slideNumber > (numberOfSlides - 1)){
        slideNumber = 0;
      }

      slides[slideNumber].classList.add("active");
      slideIcons[slideNumber].classList.add("active");
    });

    //image slider previous button
    prevBtn.addEventListener("click", () => {
      slides.forEach((slide) => {
        slide.classList.remove("active");
      });
      slideIcons.forEach((slideIcon) => {
        slideIcon.classList.remove("active");
      });

      slideNumber--;

      if(slideNumber < 0){
        slideNumber = numberOfSlides - 1;
      }

      slides[slideNumber].classList.add("active");
      slideIcons[slideNumber].classList.add("active");
    });

    //image slider autoplay
    var playSlider;

    var repeater = () => {
      playSlider = setInterval(function(){
        slides.forEach((slide) => {
          slide.classList.remove("active");
        });
        slideIcons.forEach((slideIcon) => {
          slideIcon.classList.remove("active");
        });

        slideNumber++;

        if(slideNumber > (numberOfSlides - 1)){
          slideNumber = 0;
        }

        slides[slideNumber].classList.add("active");
        slideIcons[slideNumber].classList.add("active");
      }, 4000);
    }
    repeater();

    //stop the image slider autoplay on mouseover
    slider.addEventListener("mouseover", () => {
      clearInterval(playSlider);
    });

    //start the image slider autoplay again on mouseout
    slider.addEventListener("mouseout", () => {
      repeater();
    });
              
              
    // auto fix image size
    const slideImage = document.getElementById("slider");
    const slideNavigation = document.getElementById("slide-navigation");  
    
    const slideInfo = document.querySelectorAll(".slider .slide .info");
    //console.log(slideInfo);
    function slideInfoChange(){
      slideInfo.forEach(element =>{
        element.style.marginLeft = String(slideImage.offsetWidth /10)+"px";
      }
      )
    }
    slideInfoChange();
              
    slideImage.style.height = String(slideImage.offsetWidth *34/65)+"px";  
    slideNavigation.style.height = String(slideImage.offsetHeight)+"px";  
    
    window.addEventListener('resize', function (event) {
      //console.log(slideImage.offsetHeight, slideImage.offsetWidth);
      slideImage.style.height = String(slideImage.offsetWidth *34/65)+"px";  
      slideNavigation.style.height = String(slideImage.offsetHeight)+"px"; 
      slideInfoChange();
       
    
    })
