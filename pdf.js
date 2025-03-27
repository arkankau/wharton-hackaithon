// Function to fetch and display thumbnails linked to PDFs
async function fetchAndDisplayLibrary() {
  try {
    const response = await fetch("http://localhost:3000/api/library"); // Replace with your backend endpoint
    if (!response.ok) {
      throw new Error("Failed to fetch library items");
    }

    const libraryItems = await response.json();
    const libraryList = document.querySelector(".library-list");
    libraryList.innerHTML = ""; // Clear existing content

    libraryItems.forEach((item) => {
      const libraryItem = document.createElement("div");
      libraryItem.classList.add("library-item");
      libraryItem.innerHTML = `
        <a href="${item.pdfUrl}" target="_blank">
          <img src="${item.thumbnailUrl || 'default-thumbnail.png'}" alt="${item.name}" class="library-thumbnail">
        </a>
      `;
      libraryList.appendChild(libraryItem);
    });
  } catch (error) {
    console.error("Error fetching library items:", error);
  }
}

// Fetch and display the library when the page loads
document.addEventListener("DOMContentLoaded", fetchAndDisplayLibrary);