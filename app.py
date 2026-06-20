# app.py

import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from analyzer import extract_text_from_pdf, extract_keywords, compare_keywords

# ----------------- CRUCIAL LINE -----------------
# This line creates the Flask application instance called 'app'.
# The `flask run` command looks for this variable.
# It MUST be at the top level (no indentation).
app = Flask(__name__)
# ------------------------------------------------

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'resume' not in request.files:
            return redirect(request.url)
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')

        # If the user does not select a file, the browser submits an empty file without a filename.
        if resume_file.filename == '':
            return redirect(request.url)

        if resume_file and job_description:
            # Secure the filename and save the file
            filename = secure_filename(resume_file.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(resume_path)

            # --- Core Analysis ---
            # 1. Extract text from resume PDF
            resume_text = extract_text_from_pdf(resume_path)
            
            # 2. Extract keywords from both texts
            resume_keywords = extract_keywords(resume_text)
            jd_keywords = extract_keywords(job_description)
            
            # 3. Compare keywords and get results
            analysis_result = compare_keywords(resume_keywords, jd_keywords)
            
            # Clean up the uploaded file
            os.remove(resume_path)
            
            # Render the results page
            return render_template('results.html', result=analysis_result, jd_keywords=sorted(list(jd_keywords)))

    # For a GET request, just show the main page
    return render_template('index.html')


# ----------------- CRUCIAL BLOCK -----------------
# This block allows you to run the app directly using `python app.py`
# It's an alternative to the `flask run` command.
if __name__ == '__main__':
    app.run(debug=True)
# -------------------------------------------------