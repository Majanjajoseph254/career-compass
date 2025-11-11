// DOM Elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.querySelector('.upload-btn');
const dashboardSection = document.getElementById('dashboard');
const homeSection = document.getElementById('home');

// API Endpoint
const API_BASE_URL = 'http://localhost:5000/api';

// Event Listeners
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
uploadBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    handleFiles(files);
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

// File Processing
async function handleFiles(files) {
    if (files.length === 0) return;

    const file = files[0];
    if (!validateFile(file)) {
        showError('Please upload a PDF, DOCX, or TXT file.');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('resume', file);

        showLoading();
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData,
            mode: 'cors',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        hideLoading();
        showDashboard(data);
    } catch (error) {
        hideLoading();
        showError('An error occurred during upload. Please try again.');
        console.error('Upload error:', error);
    }
}

// Validation
function validateFile(file) {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    return allowedTypes.includes(file.type);
}

// UI State Management
function showDashboard(data) {
    homeSection.classList.add('hidden');
    dashboardSection.classList.remove('hidden');
    updateDashboardData(data);
}

function updateDashboardData(data) {
    // Update charts
    updateSkillsChart(data.skills);
    updateIndustryChart(data.industries);
    
    // Update recommendations
    const recommendationsContainer = document.getElementById('career-recommendations');
    recommendationsContainer.innerHTML = data.recommendations
        .map(rec => `
            <div class="recommendation-card">
                <h4>${rec.title}</h4>
                <p>${rec.description}</p>
                <div class="match-score">Match Score: ${rec.matchScore}%</div>
            </div>
        `).join('');
}

// Loading State
function showLoading() {
    // Add loading overlay
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.innerHTML = '<div class="spinner"></div><p>Analyzing your resume...</p>';
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.loader');
    if (loader) loader.remove();
}

// Error Handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 3000);
}

// Navigation
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        document.querySelectorAll('section').forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(targetId).classList.remove('hidden');
        
        // Update active link
        document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
        link.classList.add('active');
    });
});