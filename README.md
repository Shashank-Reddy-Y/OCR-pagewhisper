
# Page Whisper - Text Extraction from PDFs & Images

**Page Whisper** is a web application that allows users to upload PDF or image files (PNG, JPG, JPEG) and extract the text contained within them using Google Cloud's Vision API. The extracted text can be downloaded in both DOCX and PDF formats.

## Features

- **Text Extraction**: Extracts text from images and PDF files.
- **File Upload**: Users can upload PNG, JPG, JPEG, and PDF files.
- **Download**: Extracted text can be downloaded as DOCX or PDF.
- **Text Preview**: Preview extracted text directly on the website.
- **Responsive**: Designed for both desktop and mobile users.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
  - Uses the Fetch API to interact with the backend.
  - Styled with custom CSS to provide a clean user interface.
- **Backend**: Flask (Python)
  - Utilizes Flask to handle file uploads, API interactions, and serving static files.
  - Uses Google Cloud Vision API for text extraction from images and PDFs.
  - Converts extracted text to DOCX and PDF formats.
- **Cloud Storage**: Google Cloud Storage (GCS)
  - For temporary file storage during the extraction process.

## Requirements

To run this project locally or deploy it, you need the following:

- Python 3.7 or above
- Flask
- Google Cloud SDK
- Required Python libraries (listed in the requirements.txt)
  
## Setup Instructions

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Shashank-Reddy-Y/OCR-pagewhisper.git
   cd OCR-pagewhisper
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up Google Cloud Vision API credentials:
   - Make sure you have the Google Cloud SDK installed and authenticated.
   - Create a Google Cloud Project and enable the Vision API and Cloud Storage.
   - Set up a service account key and export the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:
   
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account_key.json"
     ```

5. Run the Flask app:

   ```bash
   python app.py
   ```

   By default, the app will be accessible at `http://localhost:5000`.

### Frontend Setup

The frontend code is already included in the repository and works with the backend. The HTML, CSS, and JavaScript files are located in the `templates` and `static` folders.

Ensure that the static files are served correctly by Flask (Flask does this by default when the `static_folder` is defined).

### Google Cloud Storage Setup

Make sure that you have set up a Google Cloud Storage bucket and replace the `GCS_BUCKET_NAME` in the backend code (`app.py`) with the name of your bucket.

```python
GCS_BUCKET_NAME = "your-gcs-bucket-name"
```

### Folder Structure

```
page-whisper/
│
├── websitebackend.py                      # Flask backend
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Main HTML template
    --- about.html
│
└── static/
    ├── css/
    │   └── style.css           # Custom styles
        --- style_about.css
    └── js/
        └── script.js           # JavaScript for frontend functionality
```

### File Upload and Text Extraction Process

1. **Upload a file**: The user selects a PDF or image (PNG, JPG, JPEG) from their device.
2. **Text extraction**: The file is sent to the Flask backend where it is processed using the Google Cloud Vision API. The extracted text is cleaned and prepared.
3. **Download links**: Once the extraction is complete, the user is provided with download links for both DOCX and PDF formats.
4. **Text preview**: The extracted text is shown in a preview section for the user to view before downloading.

## API Endpoints

### `POST /upload`

- **Description**: Accepts file uploads (PNG, JPG, JPEG, PDF) and processes them to extract text using Google Cloud Vision API.
- **Request body**: 
  - `file` (required): The image or PDF file to upload.
  
- **Response**: 
  - `text`: Extracted text from the file.
  - `download_docx`: URL to download the extracted text as a DOCX file.
  - `download_pdf`: URL to download the extracted text as a PDF file.

### `GET /download`

- **Description**: Allows the user to download the processed file (DOCX or PDF).
- **Query parameters**: 
  - `file`: The name of the file to download.
  
- **Response**: The requested file for download.

## Troubleshooting

- **"File not found" error**: This can occur if the file is not uploaded correctly or the server has been restarted. Ensure that the file exists in the `uploads` directory.
- **Vision API errors**: If you encounter an issue with the Vision API, check your Google Cloud account's billing status and quota.
- **Make sure you connect to the Internet before running**

## Contributing

Feel free to fork the project and submit pull requests! If you find any bugs or have suggestions, please open an issue.



website demo image 

<img width="1338" alt="Screenshot 2025-03-31 at 6 27 10 PM" src="https://github.com/user-attachments/assets/5be75675-8ed7-4dbc-b0ef-75464f7a6c7e" />

<img width="1329" alt="Screenshot 2025-03-31 at 6 27 26 PM" src="https://github.com/user-attachments/assets/8d3fb3b3-f491-4667-8e89-a5e78db9acb9" />


**OUTPUTS**
| **Input Image-1** | **Output (pdf format)** |
|-------------------|-------------------------|
| ![Input1](https://github.com/user-attachments/assets/d307c024-f9b7-4d87-a8b6-2cc54db15d6f) | ![Output1](https://github.com/user-attachments/assets/0b600df2-d020-4b81-904a-17a01f0b1a74) |

| **Input Image-2** | **Output** |
|-------------------|------------|
| ![Input2](https://github.com/user-attachments/assets/14b8a7ad-b85b-4dc8-b7d7-e3aad4a34e4b) | ![Output2](https://github.com/user-attachments/assets/93a64954-e4a7-41f2-8153-0d40e0ff941c)  <img width="779" alt="Screenshot 2025-05-08 at 1 58 07 PM" src="https://github.com/user-attachments/assets/aeb2df3b-3995-4eb6-9396-3cf0fe66f8f6" />
|




---


### Notes:
AI tool like chatgpt are used for this project. The Idea was mine. Ai tools are used only for the coding part.

The google vision api has both a free trial and a paid one so, please refer to the plans before using it in your project.
