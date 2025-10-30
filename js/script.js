function matchBlockHeight() {
    const blockToAdapt = document.getElementById("starter-content");
    const imgExample = document.getElementById("main-image");
    blockToAdapt.style.height = imgExample.clientHeight + "px";
}

window.addEventListener("load", matchBlockHeight);
window.addEventListener("resize", matchBlockHeight);

