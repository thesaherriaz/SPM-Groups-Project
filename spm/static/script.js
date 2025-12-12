// Markdown parser (simple version)
function parseMarkdown(text) {
    // Convert markdown to HTML
    let html = text;
    
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    
    // Italic
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');
    
    // Links
    html = html.replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2" target="_blank">$1</a>');
    
    // Lists
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
    
    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    
    return '<p>' + html + '</p>';
}

// Global state
let currentBlogId = null;
let currentBlogData = null;
let currentTheme = localStorage.getItem('theme') || 'dark';
let blogToDelete = null;
let editingBlogId = null;

// DOM elements
const blogForm = document.getElementById('blogForm');
const generateBtn = document.getElementById('generateBtn');
const progressSection = document.getElementById('progressSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const blogSection = document.getElementById('blogSection');
const blogContent = document.getElementById('blogContent');
const editCurrentBtn = document.getElementById('editCurrentBtn');
const downloadBtn = document.getElementById('downloadBtn');
const viewDetailsBtn = document.getElementById('viewDetailsBtn');
const detailsModal = document.getElementById('detailsModal');
const closeModal = document.getElementById('closeModal');
const savedBlogs = document.getElementById('savedBlogs');
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const doneBtn = document.getElementById('doneBtn');
const editModal = document.getElementById('editModal');
const editTextarea = document.getElementById('editTextarea');
const closeEditModal = document.getElementById('closeEditModal');
const cancelEdit = document.getElementById('cancelEdit');
const saveEdit = document.getElementById('saveEdit');
const confirmDialog = document.getElementById('confirmDialog');
const cancelDelete = document.getElementById('cancelDelete');
const confirmDelete = document.getElementById('confirmDelete');

// Progress step elements
const steps = {
    1: document.getElementById('step1'),
    2: document.getElementById('step2'),
    3: document.getElementById('step3'),
    4: document.getElementById('step4')
};

// Theme functions
function setTheme(theme) {
    currentTheme = theme;
    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIcon.className = 'fas fa-sun theme-icon';
    } else {
        document.documentElement.removeAttribute('data-theme');
        themeIcon.className = 'fas fa-moon theme-icon';
    }
    localStorage.setItem('theme', theme);
}

function toggleTheme() {
    setTheme(currentTheme === 'dark' ? 'light' : 'dark');
}

// Update step status
function updateStepStatus(stepNum, status) {
    const step = steps[stepNum];
    const badge = step.querySelector('.status-badge');
    
    // Remove all status classes
    step.classList.remove('active', 'completed');
    badge.classList.remove('status-pending', 'status-processing', 'status-completed', 'status-error');
    
    // Add new status
    switch(status) {
        case 'processing':
            step.classList.add('active');
            badge.classList.add('status-processing');
            badge.textContent = 'Processing';
            break;
        case 'completed':
            step.classList.add('completed');
            badge.classList.add('status-completed');
            badge.textContent = 'Completed';
            break;
        case 'error':
            badge.classList.add('status-error');
            badge.textContent = 'Error';
            break;
        default:
            badge.classList.add('status-pending');
            badge.textContent = 'Pending';
    }
}

// Reset all steps
function resetSteps() {
    for (let i = 1; i <= 4; i++) {
        updateStepStatus(i, 'pending');
    }
}

// Show error
function showError(message) {
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
    progressSection.style.display = 'none';
}

// Hide error
function hideError() {
    errorSection.style.display = 'none';
}

// Generate blog
async function generateBlog(topic) {
    try {
        // Reset UI
        hideError();
        blogSection.style.display = 'none';
        progressSection.style.display = 'block';
        resetSteps();
        
        // Disable button
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').style.display = 'none';
        generateBtn.querySelector('.btn-loader').style.display = 'flex';
        
        // Simulate progress updates (since we're calling one endpoint)
        const progressInterval = setInterval(() => {
            // This is just visual feedback
        }, 1000);
        
        // Step 1: Research Gaps
        updateStepStatus(1, 'processing');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Step 2: Questions
        updateStepStatus(1, 'completed');
        updateStepStatus(2, 'processing');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Step 3: Methodology
        updateStepStatus(2, 'completed');
        updateStepStatus(3, 'processing');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Step 4: Blog Generation
        updateStepStatus(3, 'completed');
        updateStepStatus(4, 'processing');
        
        // Make actual API call
        const response = await fetch('/api/generate-blog', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic })
        });
        
        clearInterval(progressInterval);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate blog');
        }
        
        const data = await response.json();
        
        // Step 4 complete
        updateStepStatus(4, 'completed');
        
        // Store blog data
        currentBlogId = data.blog_id;
        currentBlogData = data;
        
        // Display blog
        displayBlog(data.content);
        
        // Hide progress, show blog
        setTimeout(() => {
            progressSection.style.display = 'none';
            blogSection.style.display = 'block';
            
            // Scroll to blog
            blogSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 1000);
        
        // Reload saved blogs
        loadSavedBlogs();
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
        
        // Mark current step as error
        for (let i = 1; i <= 4; i++) {
            const step = steps[i];
            if (step.classList.contains('active')) {
                updateStepStatus(i, 'error');
                break;
            }
        }
    } finally {
        // Re-enable button
        generateBtn.disabled = false;
        generateBtn.querySelector('.btn-text').style.display = 'inline';
        generateBtn.querySelector('.btn-loader').style.display = 'none';
    }
}

// Display blog content
function displayBlog(content) {
    // Parse markdown and display
    const htmlContent = parseMarkdown(content);
    blogContent.innerHTML = htmlContent;
}

// Download blog
async function downloadBlog() {
    if (!currentBlogId) return;
    
    try {
        const response = await fetch(`/api/blogs/${currentBlogId}/download`);
        if (!response.ok) throw new Error('Download failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `blog_${currentBlogId}.md`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Download error:', error);
        alert('Failed to download blog');
    }
}

// View details
function viewDetails() {
    if (!currentBlogData) return;
    
    // Populate modal
    document.getElementById('gapsData').textContent = 
        JSON.stringify(currentBlogData.gaps, null, 2);
    document.getElementById('questionsData').textContent = 
        JSON.stringify(currentBlogData.questions, null, 2);
    document.getElementById('methodologyData').textContent = 
        JSON.stringify(currentBlogData.methodology, null, 2);
    
    // Show modal
    detailsModal.style.display = 'flex';
}

// Edit blog
async function editBlog(blogId) {
    try {
        const response = await fetch(`/api/blogs/${blogId}`);
        const data = await response.json();
        
        editingBlogId = blogId;
        editTextarea.value = data.content;
        editModal.style.display = 'flex';
        
    } catch (error) {
        console.error('Error loading blog for edit:', error);
        alert('Failed to load blog for editing');
    }
}

// Save blog edit
async function saveBlogEdit() {
    if (!editingBlogId) return;
    
    const newContent = editTextarea.value.trim();
    if (!newContent) {
        alert('Blog content cannot be empty');
        return;
    }
    
    try {
        const response = await fetch(`/api/blogs/${editingBlogId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: newContent })
        });
        
        if (!response.ok) {
            throw new Error('Failed to update blog');
        }
        
        // Close modal
        editModal.style.display = 'none';
        
        // If this is the currently displayed blog, update it
        if (currentBlogId === editingBlogId) {
            displayBlog(newContent);
            if (currentBlogData) {
                currentBlogData.content = newContent;
            }
        }
        
        editingBlogId = null;
        
        // Show success message
        alert('Blog updated successfully!');
        
    } catch (error) {
        console.error('Error saving blog:', error);
        alert('Failed to save blog changes');
    }
}

// Delete blog
function showDeleteConfirm(blogId) {
    blogToDelete = blogId;
    confirmDialog.style.display = 'flex';
}

async function deleteBlogConfirmed() {
    if (!blogToDelete) return;
    
    try {
        const response = await fetch(`/api/blogs/${blogToDelete}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete blog');
        }
        
        // Close dialog
        confirmDialog.style.display = 'none';
        
        // If this is the currently displayed blog, hide it
        if (currentBlogId === blogToDelete) {
            blogSection.style.display = 'none';
            currentBlogId = null;
            currentBlogData = null;
        }
        
        blogToDelete = null;
        
        // Reload saved blogs
        loadSavedBlogs();
        
        // Show success message
        alert('Blog deleted successfully!');
        
    } catch (error) {
        console.error('Error deleting blog:', error);
        alert('Failed to delete blog');
    }
}

// Read blog (explicit function for read button)
async function readBlog(blogId) {
    await loadBlog(blogId);
}

// Load saved blogs
async function loadSavedBlogs() {
    try {
        const response = await fetch('/api/blogs');
        const data = await response.json();
        
        if (data.blogs.length === 0) {
            savedBlogs.innerHTML = '<p class="loading-text">No saved blogs yet</p>';
            return;
        }
        
        savedBlogs.innerHTML = data.blogs.map(blog => `
            <div class="blog-item">
                <div class="blog-item-info" data-blog-id="${blog.id}">
                    <h3>${blog.topic}</h3>
                    <p>Created: ${new Date(blog.created_at).toLocaleDateString()}</p>
                </div>
                <div class="blog-item-actions">
                    <button class="btn-icon btn-read" onclick="readBlog(${blog.id})" title="Read"><i class="fas fa-book-open"></i></button>
                    <button class="btn-icon btn-edit" onclick="editBlog(${blog.id})" title="Edit"><i class="fas fa-edit"></i></button>
                    <button class="btn-icon btn-delete" onclick="showDeleteConfirm(${blog.id})" title="Delete"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>
        `).join('');
        
        // Add click handlers for blog info area only
        document.querySelectorAll('.blog-item-info').forEach(item => {
            item.addEventListener('click', async () => {
                const blogId = item.dataset.blogId;
                await loadBlog(blogId);
            });
        });
        
    } catch (error) {
        console.error('Error loading blogs:', error);
        savedBlogs.innerHTML = '<p class="loading-text">Failed to load blogs</p>';
    }
}

// Load specific blog
async function loadBlog(blogId) {
    try {
        const response = await fetch(`/api/blogs/${blogId}`);
        const data = await response.json();
        
        currentBlogId = data.id;
        currentBlogData = {
            content: data.content,
            gaps: data.research_gaps,
            questions: data.research_questions,
            methodology: data.methodology
        };
        
        displayBlog(data.content);
        blogSection.style.display = 'block';
        blogSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Error loading blog:', error);
        alert('Failed to load blog');
    }
}

// Event listeners
blogForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const topic = document.getElementById('topic').value.trim();
    if (topic) {
        await generateBlog(topic);
    }
});

editCurrentBtn.addEventListener('click', () => {
    if (currentBlogId) {
        editBlog(currentBlogId);
    }
});

downloadBtn.addEventListener('click', downloadBlog);
viewDetailsBtn.addEventListener('click', viewDetails);

doneBtn.addEventListener('click', () => {
    blogSection.style.display = 'none';
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

closeModal.addEventListener('click', () => {
    detailsModal.style.display = 'none';
});

// Close modal on outside click
detailsModal.addEventListener('click', (e) => {
    if (e.target === detailsModal) {
        detailsModal.style.display = 'none';
    }
});

// Theme toggle
themeToggle.addEventListener('click', toggleTheme);

// Edit modal
closeEditModal.addEventListener('click', () => {
    editModal.style.display = 'none';
    editingBlogId = null;
});

cancelEdit.addEventListener('click', () => {
    editModal.style.display = 'none';
    editingBlogId = null;
});

saveEdit.addEventListener('click', saveBlogEdit);

editModal.addEventListener('click', (e) => {
    if (e.target === editModal) {
        editModal.style.display = 'none';
        editingBlogId = null;
    }
});

// Confirm dialog
cancelDelete.addEventListener('click', () => {
    confirmDialog.style.display = 'none';
    blogToDelete = null;
});

confirmDelete.addEventListener('click', deleteBlogConfirmed);

confirmDialog.addEventListener('click', (e) => {
    if (e.target === confirmDialog) {
        confirmDialog.style.display = 'none';
        blogToDelete = null;
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set initial theme
    setTheme(currentTheme);
    // Load saved blogs
    loadSavedBlogs();
});
