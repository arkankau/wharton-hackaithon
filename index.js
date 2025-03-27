// Description: This file contains the javascript code for the index.html file.

// Function to open the tab
var tablinks = document.getElementsByClassName("tab-links")
var tabcontents = document.getElementsByClassName("tab-contents")
function opentab(tabname){
    for(tablink of tablinks){
        tablink.classList.remove("active-link");
    }
    for(tabcontent of tabcontents){
        tabcontent.classList.remove("active-tab");
    }
    event.currentTarget.classList.add("active-link");
    document.getElementById(tabname).classList.add("active-tab")
}

// This function is called when the user clicks on the menu icon.
var sidemenu = document.getElementById("sidemenu");
function openmenu(){
    sidemenu.style.right = "0";
}

function closemenu(){
    sidemenu.style.right = "-200px";
}

// Login functions
// Hide the login page when any navbar option is clicked
document.querySelectorAll('nav ul li a').forEach(navItem => {
    navItem.addEventListener('click', function () {
        document.getElementById('login-page').classList.add('hidden');
    });
});

// Example list of PDFs
const pdfs = [
    { name: "Document 1", url: "pdfs/document1.pdf", thumbnail: "thumbnails/doc1.png" },
    { name: "Document 2", url: "pdfs/document2.pdf", thumbnail: "thumbnails/doc2.png" },
    { name: "Document 3", url: "pdfs/document3.pdf", thumbnail: "thumbnails/doc3.png" }
];

// Show the login page when the "Login" button is clicked
document.querySelector('.btn.btn2').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default behavior (e.g., navigation)
    const loginPage = document.getElementById('login-page');
    if (!this.classList.contains('logged-in')) {
        loginPage.classList.remove('hidden');
    }
});

// Hide the login page when clicking outside the login container
document.querySelector('#login-page').addEventListener('click', function (e) {
    const loginContainer = document.querySelector('.login-container');
    if (!loginContainer.contains(e.target)) {
      // If the click is outside the login container, hide the login page
      document.getElementById('login-page').classList.add('hidden');
    }
  });
  
  // Prevent the login form from closing the login page when clicked
  document.querySelector('.login-container').addEventListener('click', function (e) {
    e.stopPropagation(); // Stop the click event from propagating to the parent
  });

// Hide the login page when the login form is submitted and update the button text
document.querySelector('#login-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    // Get the username from the input field
    const usernameInput = document.querySelector('#login-username').value;

    if (usernameInput.trim()) {
        // Hide the login page
        document.getElementById('login-page').classList.add('hidden');

        // Update the "Login" button to display "Welcome, {username}" and disable it
        const loginButton = document.querySelector('.btn.btn2');
        loginButton.textContent = `Welcome, ${usernameInput}`; // Set the button text
        loginButton.classList.add('logged-in'); // Add the logged-in class
        loginButton.disabled = true; // Disable the button

        // Show the library
        const library = document.getElementById('library');
        library.classList.remove('hidden');

// Populate the library with PDFs
const libraryList = document.querySelector('.library-list');
libraryList.innerHTML = ""; // Clear any existing content
pdfs.forEach(pdf => {
    const libraryItem = document.createElement('div');
    libraryItem.classList.add('library-item');
    libraryItem.innerHTML = `
        <a href="${pdf.url}" target="_blank">
            <img src="${pdf.thumbnail}" alt="${pdf.name}">
        </a>
        <div class="library-layer">
            <h3>${pdf.name}</h3>
            <a href="${pdf.url}" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>
        </div>
    `;
    libraryList.appendChild(libraryItem);
});
    }
});