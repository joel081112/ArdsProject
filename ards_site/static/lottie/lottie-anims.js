/* Play an animation on each click */
/*https://lottiefiles.com/editor*/


/*singleclick .js*/

let iconSkipForward = document.querySelectorAll('.bodymovinan');
iconSkipForward.forEach(ic => {
    let animationSkipForward = bodymovin.loadAnimation({
        container: ic,
        renderer: 'svg',
        loop: false,
        autoplay: false,
        path: "https://raw.githubusercontent.com/thesvbd/Lottie-examples/master/assets/animations/skip-forward.json"
    });

    ic.addEventListener('click', function () {
        animationSkipForward.playSegments([0, 60], true);
    });
});


let iconArrowUp = document.querySelectorAll('.bodyarrowUp');
iconArrowUp.forEach(ic => {
    let animationSkipForward = bodymovin.loadAnimation({
        container: ic,
        renderer: 'svg',
        loop: false,
        autoplay: false,
        path: "lottie/json/arrow-up-circle.json"
    });

    ic.addEventListener('click', function () {
        animationSkipForward.playSegments([0, 60], true);
    });
});

/*hover .js*/
//Play an animation back on second click
/*https://lottiefiles.com/editor*/

let iconMenu = document.querySelectorAll('.bodymovi');

iconMenu.forEach( ic => {
    let animationMenu = bodymovin.loadAnimation({
            container: ic,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: "lottie/json/mail-white.json"
    });

    var directionMenu = 1;
      ic.addEventListener('mouseenter', (e) => {
      animationMenu.setDirection(directionMenu);
      animationMenu.play();
    });

      ic.addEventListener('mouseleave', (e) => {
      animationMenu.setDirection(-directionMenu);
      animationMenu.play();
    });
});

let iconLinkedIn = document.querySelectorAll('.bodylinkedIn');

iconLinkedIn.forEach( ic => {
    let animationMenu = bodymovin.loadAnimation({
            container: ic,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: "lottie/json/linkedIn.json"
    });

    var directionMenu = 1;
      ic.addEventListener('mouseenter', (e) => {
      animationMenu.setDirection(directionMenu);
      animationMenu.play();
    });

      ic.addEventListener('mouseleave', (e) => {
      animationMenu.setDirection(-directionMenu);
      animationMenu.play();
    });
});


let iconFacebook = document.querySelectorAll('.bodyfacebook');

iconFacebook.forEach( ic => {
    let animationMenu = bodymovin.loadAnimation({
            container: ic,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: "lottie/json/facebook.json"
    });

    var directionMenu = 1;
      ic.addEventListener('mouseenter', (e) => {
      animationMenu.setDirection(directionMenu);
      animationMenu.play();
    });

      ic.addEventListener('mouseleave', (e) => {
      animationMenu.setDirection(-directionMenu);
      animationMenu.play();
    });
});

let iconInfo = document.querySelectorAll('.bodyInfo');
iconInfo.forEach( ic => {
    let animationMenu = bodymovin.loadAnimation({
            container: ic,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: "lottie/json/info.json"
    });

    var directionMenu = 1;
      ic.addEventListener('mouseenter', (e) => {
      animationMenu.setDirection(directionMenu);
      animationMenu.play();
    });

      ic.addEventListener('mouseleave', (e) => {
      animationMenu.setDirection(-directionMenu);
      animationMenu.play();
    });
});

/*loader.js*/
//Animation in infinite loop
/*https://lottiefiles.com/editor*/

let svgContainer = document.querySelectorAll('.bodymovinani');
svgContainer.forEach( ic => {
    let animItem = bodymovin.loadAnimation({
        wrapper: ic,
        animType: 'svg',
        loop: true,
        path: "lottie/json/infinity.json"
    });
});

let iconArrowUpLoad = document.querySelectorAll('.bodyarrowUpload');
iconArrowUpLoad.forEach( ic => {
     bodymovin.loadAnimation({
        wrapper: ic,
        animType: 'svg',
        loop: true,
        path: "lottie/json/arrow-up-load-white.json"
    });

});

/*doubleclick .js*/
/* Lottie javascript for animation https://useanimations.com/ */
/*https://lottiefiles.com/editor*/

let iconPlus = document.querySelectorAll('.bodymovinanim');

iconPlus.forEach( ic => {

        let animationPlus = bodymovin.loadAnimation({
            container: ic,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: 'lottie/json/plustox.json'
            /* Change the path above to an animation */
        });



    var directionPlus = 1;
    ic.addEventListener('click', (e) => {
        animationPlus.setDirection(directionPlus);
        animationPlus.play();
        directionPlus = -directionPlus;
    });

});


