const analyzedtext = document.getElementById("analyzed_text");



function myFunction() {
    analyzedtext.focus();
    analyzedtext.select();
    document.execCommand("copy");
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
    // setTimeout(function () {
    //     popup.classList.remove("show");
    // }, 1000);
}
// console.log("HEllo");