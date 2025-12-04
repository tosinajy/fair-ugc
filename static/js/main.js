/**
 * FairUGC Main Logic
 * Handles Rate Calculator, Pitch Generation, and Lead Capture.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Application State ---
    const state = {
        experience_level: 'beginner',
        currentMin: 0,
        currentMax: 0,
        debounceTimer: null
    };

    // --- DOM Elements ---
    const ui = {
        // Forms & Inputs
        calcForm: document.getElementById('calcForm'),
        contentTypeInput: document.getElementById('contentType'),
        nicheInput: document.getElementById('niche'),
        expControl: document.getElementById('experienceControl'),
        expBtns: document.querySelectorAll('#experienceControl .segmented-btn'),
        usageCheckboxes: document.querySelectorAll('input[name="usage"]'),
        
        // Results Display
        resultSegment: document.getElementById('resultSegment'),
        minPriceSpan: document.getElementById('minPrice'),
        maxPriceSpan: document.getElementById('maxPrice'),
        
        // Pitch Generator
        pitchBrand: document.getElementById('pitchBrand'),
        pitchProduct: document.getElementById('pitchProduct'),
        pitchMood: document.getElementById('pitchMood'),
        generatePitchBtn: document.getElementById('generatePitchBtn'),
        pitchArea: document.getElementById('pitchArea'),
        pitchText: document.getElementById('pitchText'),
        
        // Lead Capture
        leadEmail: document.getElementById('leadEmail'),
        saveLeadBtn: document.getElementById('saveLeadBtn'),
        
        // Tools
        downloadQuoteBtn: document.getElementById('downloadQuoteBtn'),
        downloadQuoteBtnMobile: document.getElementById('downloadQuoteBtnMobile'),
        themeToggle: document.getElementById('themeToggle'),
        body: document.body
    };

    // --- Initialization ---
    initTheme();
    initSemanticUI();
    bindEvents();

    // ---------------------------------------------------------
    // 1. Initialization & Events
    // ---------------------------------------------------------

    function initSemanticUI() {
        // Initialize dropdowns with callbacks
        $('.ui.dropdown').dropdown({ 
            onChange: triggerCalculation 
        });
        $('.ui.checkbox').checkbox();
    }

    function initTheme() {
        const savedTheme = localStorage.getItem('fairugc-theme');
        if (savedTheme === 'dark') {
            ui.body.classList.add('dark-mode');
            if(ui.themeToggle) ui.themeToggle.innerHTML = '<i class="sun icon"></i> Light Mode';
        }
    }

    function bindEvents() {
        // Theme Toggle
        if(ui.themeToggle) {
            ui.themeToggle.addEventListener('click', toggleTheme);
        }

        // Experience Level Switcher
        ui.expBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Update UI
                ui.expBtns.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                
                // Update State
                state.experience_level = e.target.dataset.value;
                updateExperienceHelper(state.experience_level);
                
                triggerCalculation();
            });
        });

        // Usage Rights Checkboxes
        ui.usageCheckboxes.forEach(cb => {
            cb.addEventListener('change', triggerCalculation);
        });

        // Action Buttons
        if(ui.generatePitchBtn) ui.generatePitchBtn.addEventListener('click', handlePitchGeneration);
        if(ui.saveLeadBtn) ui.saveLeadBtn.addEventListener('click', handleLeadCapture);
        if(ui.downloadQuoteBtn) ui.downloadQuoteBtn.addEventListener('click', generatePDF);
        if(ui.downloadQuoteBtnMobile) ui.downloadQuoteBtnMobile.addEventListener('click', generatePDF);
    }

    // ---------------------------------------------------------
    // 2. Logic & API Calls
    // ---------------------------------------------------------

    function toggleTheme() {
        ui.body.classList.toggle('dark-mode');
        const isDark = ui.body.classList.contains('dark-mode');
        ui.themeToggle.innerHTML = isDark ? '<i class="sun icon"></i> Light Mode' : '<i class="moon icon"></i> Dark Mode';
        localStorage.setItem('fairugc-theme', isDark ? 'dark' : 'light');
    }

    function updateExperienceHelper(level) {
        const helper = document.getElementById('expHelper');
        if(!helper) return;
        
        const texts = {
            'beginner': "Beginner: Portfolio building, under 6 months exp.",
            'intermediate': "Intermediate: Proven track record, good lighting/audio.",
            'pro': "Pro: High conversion rates, premium equipment."
        };
        helper.textContent = texts[level] || "";
    }

    // Debounce the calculation to prevent spamming the API
    function triggerCalculation() {
        clearTimeout(state.debounceTimer);
        state.debounceTimer = setTimeout(performCalculation, 500); 
    }

    async function performCalculation() {
        // Gather Data
        const selectedRights = Array.from(document.querySelectorAll('input[name="usage"]:checked'))
                                    .map(cb => cb.value);

        const payload = {
            content_type: ui.contentTypeInput.value,
            niche: ui.nicheInput.value,
            experience_level: state.experience_level,
            usage_rights: selectedRights
        };

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();

            if (!response.ok) {
                // Graceful Error Handling: Check for validation messages
                console.error("Calculation Error:", data);
                // Optional: Display toast or error message on UI
                return;
            }
            
            // Update State
            state.currentMin = data.min_price;
            state.currentMax = data.max_price;
            
            // Update UI
            animateValue(ui.minPriceSpan, parseInt(ui.minPriceSpan.textContent), state.currentMin, 500);
            animateValue(ui.maxPriceSpan, parseInt(ui.maxPriceSpan.textContent), state.currentMax, 500);
            
            if (ui.resultSegment.style.display === 'none') {
                $(ui.resultSegment).fadeIn();
            }
            
        } catch (err) {
            console.error("Network Error:", err);
        }
    }

    async function handlePitchGeneration() {
        const btn = ui.generatePitchBtn;
        btn.classList.add('loading');
        
        const brand = ui.pitchBrand.value || "[Brand Name]";
        const product = ui.pitchProduct.value || "[Product]";
        const mood = ui.pitchMood.value;
        
        try {
            const response = await fetch('/api/pitch/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mood: mood })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                let content = data.content;
                // Client-side template injection
                content = content.replace(/{brand_name}/g, brand)
                                 .replace(/{product_type}/g, product)
                                 .replace(/\[Your Name\]/g, "");
                
                ui.pitchText.value = content;
                $(ui.pitchArea).slideDown();
            } else {
                alert("Error generating pitch. Please try again.");
            }
        } catch(e) {
            console.error(e);
            alert("Network error. Please check your connection.");
        } finally {
            btn.classList.remove('loading');
        }
    }

    async function handleLeadCapture() {
        const email = ui.leadEmail.value;
        const btn = ui.saveLeadBtn;

        if(!email || !email.includes('@')) {
            alert("Please enter a valid email address.");
            return;
        }
        
        btn.classList.add('loading');
        
        try {
            const response = await fetch('/api/lead', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });

            if (response.ok) {
                btn.textContent = "Saved!";
                btn.classList.add('disabled', 'green');
                btn.classList.remove('violet');
            } else {
                const err = await response.json();
                alert(err.email ? err.email[0] : "Could not save email.");
            }
        } catch(e) {
            console.error(e);
            alert("An error occurred. Please try again.");
        } finally {
            btn.classList.remove('loading');
        }
    }

    // ---------------------------------------------------------
    // 3. Utilities
    // ---------------------------------------------------------

    function generatePDF() {
        if (!window.jspdf) {
            alert("PDF Generator not loaded.");
            return;
        }
        
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        const date = new Date().toLocaleDateString();
        const type = ui.contentTypeInput.value.toUpperCase();
        
        // Header
        doc.setFontSize(22);
        doc.text("FairUGC Rate Quote", 20, 20);
        
        doc.setFontSize(12);
        doc.text(`Date: ${date}`, 20, 30);
        doc.setLineWidth(0.5);
        doc.line(20, 35, 190, 35);
        
        // Details
        doc.setFontSize(14);
        doc.text("Project Details:", 20, 45);
        doc.setFontSize(12);
        doc.text(`• Content Type: ${type}`, 25, 55);
        doc.text(`• Niche: ${ui.nicheInput.value}`, 25, 62);
        doc.text(`• Experience: ${state.experience_level}`, 25, 69);
        
        // Rights
        doc.text("Selected Usage Rights:", 20, 80);
        const checkboxes = document.querySelectorAll('input[name="usage"]:checked');
        let yPos = 87;
        
        if(checkboxes.length === 0) {
            doc.text(`• Organic Only`, 25, yPos);
        } else {
            checkboxes.forEach(cb => {
                // Find label text associated with checkbox
                const label = cb.nextElementSibling ? cb.nextElementSibling.innerText : cb.value;
                doc.text(`• ${label}`, 25, yPos);
                yPos += 7;
            });
        }
        
        // Price
        doc.setFontSize(16);
        doc.setTextColor(99, 102, 241); // Primary Indigo Color
        doc.text(`Estimated Rate: $${state.currentMin} - $${state.currentMax}`, 20, yPos + 15);
        
        // Footer disclaimer
        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text("This quote is an estimate generated by FairUGC.", 20, 280);
        
        doc.save("FairUGC_Quote.pdf");
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});