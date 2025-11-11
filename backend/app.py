from flask import Flask, request, jsonify
from flask_cors import CORS
from api.resume_parser import parse_resume
from api.job_matcher import match_jobs
from utils.file_handler import save_upload
import os
import logging

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8080"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure Flask
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    try:
        # Log the incoming request
        app.logger.info('Received file upload request')
        
        if 'resume' not in request.files:
            app.logger.error('No file part in the request')
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            app.logger.error('No selected file')
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            app.logger.error(f'Invalid file type: {file.filename}')
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT files only.'}), 400
        
        try:
            # Save the file
            filepath = save_upload(file, app.config['UPLOAD_FOLDER'])
            app.logger.info(f'File saved successfully: {filepath}')
            
            # Parse resume
            app.logger.info('Starting resume parsing')
            resume_data = parse_resume(filepath)
            app.logger.info('Resume parsed successfully')
            
            # Get job matches
            app.logger.info('Starting job matching')
            job_matches = match_jobs(resume_data)
            app.logger.info('Job matching completed')
            
            response_data = {
                'skills': resume_data['skills'],
                'industries': job_matches['industries'],
                'recommendations': job_matches['recommendations']
            }
            
            # Clean up the uploaded file
            try:
                os.remove(filepath)
            except Exception as e:
                app.logger.warning(f'Failed to remove uploaded file: {str(e)}')
            
            return jsonify(response_data)
            
        except Exception as e:
            app.logger.error(f'Error processing file: {str(e)}')
            raise
    
    except Exception as e:
        app.logger.error(f'Upload error: {str(e)}')
        return jsonify({
            'error': 'An error occurred while processing your resume',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    health_status = {
        'status': 'healthy',
        'dependencies': {}
    }
    
    # Check spaCy
    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
        health_status['dependencies']['spacy'] = 'healthy'
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['dependencies']['spacy'] = str(e)
    
    # Check scikit-learn
    try:
        import sklearn
        health_status['dependencies']['scikit-learn'] = 'healthy'
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['dependencies']['scikit-learn'] = str(e)
    
    # Check upload directory
    try:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        if os.access(app.config['UPLOAD_FOLDER'], os.W_OK):
            health_status['dependencies']['upload_folder'] = 'healthy'
        else:
            raise Exception('Upload folder not writable')
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['dependencies']['upload_folder'] = str(e)
    
    return jsonify(health_status)

if __name__ == '__main__':
    app.run(debug=True)