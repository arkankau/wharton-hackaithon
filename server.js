const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

// Serve static files
app.use("/pdfs", express.static(path.join(__dirname, "pdfs")));
app.use("/thumbnails", express.static(path.join(__dirname, "thumbnails")));

// Endpoint to get the list of PDFs and thumbnails
app.get("/api/library", (req, res) => {
  const pdfFolder = path.join(__dirname, "pdfs");
  const thumbnailFolder = path.join(__dirname, "thumbnails");

  // Read the files in the PDFs folder
  fs.readdir(pdfFolder, (err, pdfFiles) => {
    if (err) {
      return res.status(500).json({ error: "Failed to read PDFs folder" });
    }

    // Read the files in the Thumbnails folder
    fs.readdir(thumbnailFolder, (err, thumbnailFiles) => {
      if (err) {
        return res.status(500).json({ error: "Failed to read Thumbnails folder" });
      }

      // Match PDFs with their corresponding thumbnails
      const libraryItems = pdfFiles.map((pdfFile) => {
        const thumbnailFile = thumbnailFiles.find((thumb) =>
          thumb.startsWith(path.parse(pdfFile).name)
        );
        return {
          name: path.parse(pdfFile).name,
          pdfUrl: `/pdfs/${pdfFile}`,
          thumbnailUrl: thumbnailFile ? `/thumbnails/${thumbnailFile}` : null,
        };
      });

      res.json(libraryItems);
    });
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});