// Basic Drag & Drop Functionality - Add this to your main.js or create a new file

class DocumentUploader {
  constructor() {
    // Get DOM elements
    this.dropZone = document.getElementById('dropzone');
    this.fileInput = document.getElementById('fileInput');
    this.uploadStatus = document.getElementById('uploadStatus');
    this.isProcessing = false; // file processing flag
    this.uploadEndpoint = '/user_uploads/upload-document';

    // File validation settings
    this.maxFileSize = 10 * 1024 * 1024; // 10MB in bytes
    this.allowedTypes = [
        'application/pdf',                    // .pdf
        'application/msword',                 // .doc
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
        'text/plain'                         // .txt
    ];

    

    // Only initialize if elements exist (user is logged in)
    if (this.dropZone && this.fileInput && this.uploadStatus) {
      this.initializeEventListeners();
      console.log('Document uploader initialized');
    }
  }

  initializeEventListeners() {
    // Drag and drop events
    this.dropZone.addEventListener('dragenter', (e) => this.handleDragEnter(e));
    this.dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
    this.dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
    this.dropZone.addEventListener('drop', (e) => this.handleDrop(e));
    
    // Click to select files
    this.dropZone.addEventListener('click', () => this.handleClick());
    this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    
    console.log('Event listeners attached');
  }

  // STEP 1: Handle drag enter (when file first enters the drop zone)
  handleDragEnter(e) {
    console.log('Drag enter');
    e.preventDefault();
    e.stopPropagation();
    
    // Add visual feedback
    this.dropZone.classList.add('dragover');
  }

  // STEP 2: Handle drag over (while hovering over drop zone)
  handleDragOver(e) {
    console.log('Drag over');
    e.preventDefault(); // This is CRUCIAL - allows dropping
    e.stopPropagation();
    
    // Maintain visual feedback
    this.dropZone.classList.add('dragover');
  }

  // STEP 3: Handle drag leave (when dragging away from drop zone)
  handleDragLeave(e) {
    console.log('Drag leave');
    e.preventDefault();
    e.stopPropagation();
    
    // Only remove visual feedback if truly leaving the drop zone
    // (not just moving between child elements)
    if (!this.dropZone.contains(e.relatedTarget)) {
      this.dropZone.classList.remove('dragover');
    }
  }

  // STEP 4: Handle drop (when files are dropped)
  handleDrop(e) {
    console.log('📂 Files dropped!');
    e.preventDefault();
    e.stopPropagation();
    
    // Prevent double processing
    if (this.isProcessing) {
      console.log('⏸️ Already processing, ignoring duplicate');
      return;
    }
    
    this.dropZone.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    console.log(`📁 Received ${files.length} files:`, files);
    
    if (files.length > 0) {
      this.processFiles(files);
    }
  }

  // STEP 5: Handle click (alternative to dragging)
  handleClick() {
    console.log('🖱️ Drop zone clicked');
    // Prevent any drag events from interfering
    this.dropZone.classList.remove('dragover');
    this.fileInput.click();
  }

  // STEP 6: Handle file selection via click
  handleFileSelect(e) {
    console.log('📁 Files selected via click');
    
    // Prevent double processing
    if (this.isProcessing) {
      console.log('⏸️ Already processing, ignoring duplicate');
      return;
    }
    
    const files = Array.from(e.target.files);
    console.log(`📁 Selected ${files.length} files:`, files);
    
    if (files.length > 0) {
      this.processFiles(files);
    }
    
    // Clear the input value to allow selecting the same file again
    e.target.value = '';
  }

  // STEP 7: Process the files and validate
  processFiles(files) {
    console.log('⚙️ Processing files:', files);
    
    // Set processing flag
    this.isProcessing = true;
    
    if (files.length === 0) {
        this.showStatus('No files selected', 'error');
        this.isProcessing = false; // Reset flag
        return;
    }

    // Validate each file
    const validFiles = [];
    const invalidFiles = [];
    
    files.forEach(file => {
        if (this.validateFile(file)) {
            validFiles.push(file);
        } else {
            invalidFiles.push(file);
        }
    });

    // Show validation results
    if (invalidFiles.length > 0) {
        const fileNames = invalidFiles.map(file => file.name).join(', ');
        this.showStatus(`❌ Invalid files: ${fileNames}`, 'error');
    }

    // Upload valid files
    if (validFiles.length > 0) {
        const fileNames = validFiles.map(file => `${file.name} (${this.formatFileSize(file.size)})`).join(', ');
        this.showStatus(`🔄 Uploading: ${fileNames}`, 'info');
        
        this.uploadFiles(validFiles);
    } else {
        // No valid files, reset flag
        this.isProcessing = false;
    }
  }

  // STEP 8: Upload files to server (MISSING METHOD - NOW ADDED)
  async uploadFiles(files) {
    console.log('📤 Starting upload for files:', files.map(f => f.name));
    
    try {
      // Create upload promises for each file
      const uploadPromises = files.map(file => this.uploadSingleFile(file));
      
      // Wait for all uploads to complete
      const results = await Promise.allSettled(uploadPromises);
      
      // Handle the results
      this.handleUploadResults(results, files);
      
    } catch (error) {
      console.error('❌ Upload process failed:', error);
      this.showStatus(`❌ Upload failed: ${error.message}`, 'error');
      this.isProcessing = false;
    }
  }

    // NEW: Add file validation function
  validateFile(file) {
    console.log(`🔍 Validating file: ${file.name} (${file.size} bytes, ${file.type})`);
    
    // Check file size
    if (file.size > this.maxFileSize) {
        console.log(`❌ File too large: ${file.name} (${this.formatFileSize(file.size)} > ${this.formatFileSize(this.maxFileSize)})`);
        return false;
    }
    
    // Check file type
    if (!this.allowedTypes.includes(file.type)) {
        console.log(`❌ Invalid file type: ${file.name} (${file.type})`);
        return false;
    }
    
    console.log(`✅ File valid: ${file.name}`);
    return true;
  }

    // NEW: Add helper function to format file sizes
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  showStatus(message, type = 'info') {
    console.log(`📢 Status [${type}]: ${message}`);
    
    // Define colors for different message types
    const colors = {
      'info': { bg: '#d1ecf1', text: '#0c5460' },
      'success': { bg: '#d4edda', text: '#155724' },
      'error': { bg: '#f8d7da', text: '#721c24' }
    };
    
    const color = colors[type] || colors['info'];
    
    // Display the message
    this.uploadStatus.innerHTML = `
      <div style="
        padding: 10px; 
        margin: 5px 0; 
        border-radius: 4px; 
        background-color: ${color.bg};
        color: ${color.text};
        font-size: 13px;
        border-left: 4px solid ${color.text};
      ">
        ${message}
      </div>
    `;

    // Auto-hide info and success messages after 3 seconds
    if (type === 'info' || type === 'success') {
      setTimeout(() => {
        this.uploadStatus.innerHTML = '';
      }, 3000);
    }
  }

  async uploadSingleFile(file) {
    return new Promise((resolve, reject) => {
      const formData = new FormData();
      formData.append('file', file);
      
      const xhr = new XMLHttpRequest();
      
      // Show upload progress
      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          const percentComplete = (e.loaded / e.total) * 100;
          this.showStatus(
            `🔄 Uploading ${file.name}: ${percentComplete.toFixed(1)}%`, 
            'info'
          );
        }
      };
      
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            
            // FastAPI returns complete result immediately!
            if (response.ready_for_chat) {
              this.showStatus(
                `✅ ${file.name} uploaded and ready for chat!`, 
                'success'
              );
            }
            
            resolve({
              file: file,
              response: response,
              status: 'success'
            });
            
          } catch (parseError) {
            reject(new Error(`Failed to parse response: ${parseError}`));
          }
        } else {
          reject(new Error(`Upload failed: ${xhr.status} ${xhr.statusText}`));
        }
      };
      
      xhr.onerror = () => reject(new Error(`Network error uploading ${file.name}`));
      
      // Important: Set longer timeout for processing
      xhr.timeout = 120000; // 2 minutes instead of 30 seconds
      xhr.ontimeout = () => reject(new Error(`Processing timeout for ${file.name}`));
      
      xhr.open('POST', this.uploadEndpoint, true);
      xhr.send(formData);
    });
  }

  handleUploadResults(results, files) {
    const successful = results.filter(r => r.status === 'fulfilled');
    const failed = results.filter(r => r.status === 'rejected');

    if (successful.length > 0) {
      const count = successful.length;
      this.showStatus(
        `🎉 ${count} document${count > 1 ? 's' : ''} ready for chat!`, 
        'success'
      );
      
      // No polling needed - everything is already done!
      this.onUploadSuccess && this.onUploadSuccess(successful.map(r => r.value));
    }

    if (failed.length > 0) {
      const errorMessages = failed.map(result => result.reason.message);
      this.showStatus(`❌ Upload failed: ${errorMessages.join(', ')}`, 'error');
    }

    this.isProcessing = false;
    this.fileInput.value = '';
  }

}

// Initialize when the page loads AND when user logs in
let documentUploader = null;

// Function to initialize uploader (call this when chat becomes visible)
function initializeUploader() {
  documentUploader = new DocumentUploader();
}

// Try to initialize immediately (in case user is already logged in)
document.addEventListener('DOMContentLoaded', () => {
  initializeUploader();
});

// Export for use in your main.js if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DocumentUploader, initializeUploader };
}
