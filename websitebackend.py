from flask import Flask, request, jsonify, send_file, render_template
import json
import re
from google.cloud import vision, storage
from docx import Document
from fpdf import FPDF
import io
import os
import time
from flask_cors import CORS

# After initializing your Flask app
def delete_from_gcs(bucket_name, file_name):
    """Delete a file from Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print(f"Deleted {file_name} from {bucket_name}")

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)
GCS_BUCKET_NAME = "vision-api-bucket-123"

def detect_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f"Error in Vision API: {response.error.message}")
    detected_text = response.text_annotations[0].description if response.text_annotations else "No text found"
    return detected_text

def clean_text(text):
    """
    Cleans extracted text by merging broken lines while preserving paragraphs.
    - Keeps paragraph breaks (detects empty lines as paragraph separators).
    - Merges only broken sentences.
    - Keeps proper formatting for bullet points and headings.
    """

    lines = text.split("\n")
    cleaned_lines = []
    buffer_line = ""
    previous_was_empty = True  # To track paragraph breaks

    for i in range(len(lines)):
        line = lines[i].strip()

        # Detect paragraph breaks (empty lines)
        if not line:
            if not previous_was_empty:
                cleaned_lines.append("")  # Preserve paragraph break
            previous_was_empty = True
            continue

        # Check if we should merge this line with the previous one
        if buffer_line:
            if (
                not re.match(r".*[\.\?!]$", buffer_line)  # Previous line doesn’t end with punctuation
                and not re.match(r"^[A-Z0-9•-]", line)   # This line doesn’t look like a new paragraph/heading
            ):
                buffer_line += " " + line  # Merge with previous
                continue
            else:
                cleaned_lines.append(buffer_line)
                buffer_line = line
        else:
            buffer_line = line

        previous_was_empty = False  # Reset paragraph tracker

    # Append last buffered line
    if buffer_line:
        cleaned_lines.append(buffer_line)

    return "\n".join(cleaned_lines)



def detect_text_from_pdf(gcs_uri):
    """Extracts text from a PDF file stored in GCS using Google Vision API."""
    client = vision.ImageAnnotatorClient()

    gcs_source = vision.GcsSource(uri=gcs_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type="application/pdf")

    output_uri = f"{gcs_uri}-output/"
    gcs_destination = vision.GcsDestination(uri=output_uri)
    output_config = vision.OutputConfig(gcs_destination=gcs_destination, batch_size=5)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)],
        input_config=input_config,
        output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])
    operation.result(timeout=300)  # Wait for processing to complete

    # Fetch the output from GCS
    storage_client = storage.Client()
    bucket_name = gcs_uri.split("/")[2]  # Extract bucket name
    prefix = gcs_uri.split("/")[-1] + "-output/"  # Extract output folder prefix
    bucket = storage_client.bucket(bucket_name)

    text = ""
    json_files = []  # Store JSON filenames for deletion

    for blob in bucket.list_blobs(prefix=prefix):
        if blob.name.endswith(".json"):
            json_files.append(blob)  # Store for deletion
            json_data = json.loads(blob.download_as_text())

            # Check if "responses" key exists
            if "responses" not in json_data:
                print(f"Warning: 'responses' key missing in {blob.name} {json_data}")
                continue  # Skip this JSON file

            for response in json_data.get("responses", []):
                if "fullTextAnnotation" in response:
                    text += response["fullTextAnnotation"]["text"] + "\n\n"

            # for response in json_data["responses"]:
            #     if "fullTextAnnotation" in response:
            #         text += response["fullTextAnnotation"]["text"] + "\n\n"

    # Delete JSON files after processing
    for blob in json_files:
        blob.delete()
        print(f"Deleted {blob.name} from {bucket_name}")
    text = clean_text(text)

    return text 


def upload_to_gcs(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    return f"gs://{bucket_name}/{blob.name}", blob.name

def save_as_docx(text, output_path):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_path)

def save_as_pdf(text, output_path):
    """Save extracted text as a PDF using UTF-8 encoding."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_font("DejaVu", "", "/Users/apple/Documents/fonts/DejaVuSans.ttf", uni=True)  # Ensure correct font
    pdf.set_font("DejaVu", size=12)
    
    pdf.multi_cell(0, 10, text.encode("utf-8").decode("utf-8"))  # Fix encoding issue
    pdf.output(output_path, "F")


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)
    
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = detect_text_from_image(file_path)
    elif filename.lower().endswith('.pdf'):
        gcs_uri, gcs_file_name = upload_to_gcs(GCS_BUCKET_NAME, file_path)
        text = detect_text_from_pdf(gcs_uri)
        delete_from_gcs(GCS_BUCKET_NAME, gcs_file_name)  # Automatically delete from GCS
    else:
        return jsonify({"error": "Only images and PDFs are supported."}), 400
    
    docx_path = file_path.replace('.jpg', '.docx').replace('.png', '.docx').replace('.pdf', '.docx')
    pdf_path = file_path.replace('.jpg', '.pdf').replace('.png', '.pdf').replace('.pdf', '_output.pdf')
    
    save_as_docx(text, docx_path)
    save_as_pdf(text, pdf_path)
    
    return jsonify({
        "text": text,
        "download_docx": f"/download?file={os.path.basename(docx_path)}",
        "download_pdf": f"/download?file={os.path.basename(pdf_path)}"
    })

@app.route("/download", methods=["GET"])
def download_file():
    filename = request.args.get("file")
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
