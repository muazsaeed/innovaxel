// DOM Elements
const shortenForm = document.getElementById('shorten-form');
const urlInput = document.getElementById('url-input');
const resultContainer = document.getElementById('result-container');
const shortenedUrlInput = document.getElementById('shortened-url');
const originalUrlSpan = document.getElementById('original-url');
const createdDateSpan = document.getElementById('created-date');
const copyButton = document.getElementById('copy-button');
const statsButton = document.getElementById('stats-button');
const newUrlButton = document.getElementById('new-url-button');
const statsContainer = document.getElementById('stats-container');
const statShortcode = document.getElementById('stat-shortcode');
const statCreated = document.getElementById('stat-created');
const statUpdated = document.getElementById('stat-updated');
const statAccessCount = document.getElementById('stat-access-count');
const backButton = document.getElementById('back-button');

// Current URL data
let currentUrlData = null;

// Event Listeners
shortenForm.addEventListener('submit', handleShortenUrl);
copyButton.addEventListener('click', handleCopy);
statsButton.addEventListener('click', handleViewStats);
newUrlButton.addEventListener('click', handleNewUrl);
backButton.addEventListener('click', handleBack);

// Functions
async function handleShortenUrl(e) {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'An error occurred');
        }
        
        const data = await response.json();
        currentUrlData = data;
        
        // Display the shortened URL
        const shortenedUrl = `${window.location.origin}/${data.shortCode}`;
        shortenedUrlInput.value = shortenedUrl;
        originalUrlSpan.textContent = data.url;
        
        // Format and display the creation date
        const createdDate = new Date(data.createdAt);
        createdDateSpan.textContent = formatDate(createdDate);
        
        // Show the result container
        resultContainer.classList.remove('hidden');
        
        // Hide the stats container if it's visible
        statsContainer.classList.add('hidden');
    } catch (error) {
        showError(error.message);
    }
}

async function handleViewStats() {
    if (!currentUrlData) return;
    
    try {
        const response = await fetch(`/shorten/${currentUrlData.shortCode}/stats`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'An error occurred');
        }
        
        const statsData = await response.json();
        
        // Update the stats display
        statShortcode.textContent = statsData.shortCode;
        statCreated.textContent = formatDate(new Date(statsData.createdAt));
        statUpdated.textContent = formatDate(new Date(statsData.updatedAt));
        statAccessCount.textContent = statsData.accessCount;
        
        // Show the stats container and hide the result container
        statsContainer.classList.remove('hidden');
        resultContainer.classList.add('hidden');
    } catch (error) {
        showError(error.message);
    }
}

function handleNewUrl() {
    // Clear the form and hide the result container
    shortenForm.reset();
    resultContainer.classList.add('hidden');
    statsContainer.classList.add('hidden');
    currentUrlData = null;
}

function handleBack() {
    // Hide stats and show result
    statsContainer.classList.add('hidden');
    resultContainer.classList.remove('hidden');
}

async function handleCopy() {
    const textToCopy = shortenedUrlInput.value;
    
    try {
        await navigator.clipboard.writeText(textToCopy);
        
        // Visual feedback
        const originalText = copyButton.innerHTML;
        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        
        setTimeout(() => {
            copyButton.innerHTML = originalText;
        }, 2000);
    } catch (error) {
        console.error('Failed to copy: ', error);
    }
}

function formatDate(date) {
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showError(message) {
    alert(message);
} 