function matchBlockHeights() {
    document.querySelectorAll(".matchHeights").forEach(section => {
        const image = section.querySelector(".bg-img");
        if(image){
            section.style.height = image.clientHeight + "px";
            console.log("Image is present");
            console.log(image.clientHeight + "px")
        }
    });
}


window.addEventListener("load", matchBlockHeights);
window.addEventListener("resize", matchBlockHeights);
