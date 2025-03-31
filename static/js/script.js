
// document.getElementById('uploadForm').addEventListener('submit', function (event) {
//     event.preventDefault();  // Prevent form submission

//     const formData = new FormData();
//     const fileInput = document.getElementById('file');

//     if (fileInput.files.length === 0) {
//         alert('Please select a file to upload.');
//         return;
//     }

//     formData.append('file', fileInput.files[0]);

//     // Show loading message
//     document.getElementById('extractedText').textContent = 'Processing your file, please wait...';

//     fetch('http://localhost:5000/upload', {
//         method: 'POST',
//         body: formData,
//         timeout: 60000
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             document.getElementById('extractedText').textContent = `Error: ${data.error}`;
//             document.getElementById('downloadLinks').style.display = 'none';
//         } else {
//             document.getElementById('extractedText').textContent = data.text || 'No text detected';
//             document.getElementById('downloadDocx').href = data.download_docx;
//             document.getElementById('downloadPdf').href = data.download_pdf;
//             document.getElementById('downloadLinks').style.display = 'block';
//         }
//     })
//     .catch(error => {
//         document.getElementById('extractedText').textContent = `Error: ${error.message}`;
//         document.getElementById('downloadLinks').style.display = 'none';
//     });
// });
document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    // Disable the upload button and show "Processing..." message
    const uploadButton = document.getElementById('uploadForm');
    const processingMessage = document.getElementById('processingMessage');
    const formContainer = document.querySelector(".form-container");
    const downloadLinks = document.querySelector(".download-links");
    const textPreviewSection = document.getElementById("textPreviewSection");
    const textPreview = document.getElementById("textPreview");

    // Hide the form and show processing message
    uploadButton.style.display = 'none';
    processingMessage.style.display = 'block';
    
    // Create a new FormData object to handle the file
    const formData = new FormData();
    const fileInput = document.getElementById('file');
    
    if (fileInput.files.length === 0) {
        alert('Please select a file to upload.');
        return;
    }

    formData.append("file", fileInput.files[0]);

    // Send the file to the backend API
    fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
        timeout: 60000 // Set a timeout for the request (60 seconds)
    })
    .then((response) => response.json())
    .then((data) => {
        // If there is an error, display it
        if (data.error) {
            alert("Error: " + data.error);
            processingMessage.style.display = 'none';
            uploadButton.disabled = false;
            uploadButton.style.display = 'inline-block';
            return;
        } else {
            // Hide the form and show the download links
            formContainer.style.display = "none";
            downloadLinks.style.display = "block";

            // Display the download links
            document.getElementById('downloadDocx').href = data.download_docx;
            document.getElementById('downloadPdf').href = data.download_pdf;

            // Show the text preview section
            textPreviewSection.style.display = "block";

            // Insert the extracted text into the preview section
            textPreview.textContent = data.text; // Or use textPreview.innerHTML if it's formatted HTML text

            // Hide processing message and show the upload button again
            processingMessage.style.display = 'none';
            uploadButton.disabled = false;
            uploadButton.style.display = 'inline-block';
        }
    })
    .catch((error) => {
        alert("Failed to upload file: " + error);
        processingMessage.style.display = 'none';
        uploadButton.disabled = false;
        uploadButton.style.display = 'inline-block';
    });
});

