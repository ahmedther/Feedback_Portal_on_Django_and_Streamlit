

// Get the overlay and close button elements
const overlay = document.querySelector('.overlay');
const closeButton = document.querySelector('.close-btn');

if (overlay) {// Attach a click event listener to the overlay and close button elements
    overlay.addEventListener('click', removeOverlay);
    closeButton.addEventListener('click', removeOverlay);

    // Event listener function to remove the overlay element from the DOM
    function removeOverlay(event) {
        // Check if the clicked element is the overlay or the close button
        if (event.target === overlay || event.target === closeButton) {
            // Remove the overlay element from the DOM
            overlay.remove();
        }
    }
}




function submitButtonClick() {
    const link = document.getElementById('anchor-to-submit');
    const form = document.getElementById('uhid_form');

    link.addEventListener('click', function (event) {
        event.preventDefault();
        form.submit();
    });
}


submitButtonClick()