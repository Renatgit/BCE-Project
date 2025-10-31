function matchBlockHeight() {
    const blockToAdapt = document.getElementById("starter-content");
    const imgExample = document.getElementById("main-image");
    blockToAdapt.style.minHeight = imgExample.clientHeight + "px";
    console.log(imgExample.clientHeight + "px");
}

window.addEventListener("load", matchBlockHeight);
window.addEventListener("resize", matchBlockHeight);

