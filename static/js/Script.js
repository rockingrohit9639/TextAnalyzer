
function copyToClipboard(elementId) {

    // Create an auxiliary hidden input
    var aux = document.createElement("input");
  
    // Get the text from the element passed into the input
    aux.setAttribute("value", document.getElementById(elementId).innerHTML);
  
    // Append the aux input to the body
    document.body.appendChild(aux);
  
    // Highlight the content
    aux.select();
  
    // Execute the copy command
    document.execCommand("copy");
  
    // Remove the input from the body
    document.body.removeChild(aux); 
}

console.log("This is injected")



/*===== SCROLL REVEAL ANIMATION =====*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '80px',
    duration: 2000,
    reset: true
})

/*===== SCROLL REVEAL ANIMATION-CARDS =====*/
sr.reveal('.generate-password', {})
sr.reveal('.sentiment-analysis', {delay: 200})
sr.reveal('.search-images', { delay: 400})

/*===== SCROLL REVEAL ANIMATION-HEADER =====*/
sr.reveal('.header__left', {origin:'left'})
sr.reveal('.header__right', {origin:'right'})


/*===== SCROLL REVEAL ANIMATION-CONTACT FORM =====*/
sr.reveal('.contact-form', {})
sr.reveal('.icons', {})

/*===== SCROLL REVEAL ANIMATION-CONTRIBUTER =====*/
sr.reveal('.user-names', {})
sr.reveal('.rounded-circle', {delay: 200})