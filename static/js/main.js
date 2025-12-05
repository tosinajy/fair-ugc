document.addEventListener('DOMContentLoaded', () => {
    
    const config = { debounceTime: 300 };
    let state = {
        contentType: 'video_1',
        niche: 'lifestyle',
        experience: 'beginner',
        timer: null
    };

    const els = {
        // Inputs
        pills: document.querySelectorAll('.type-pill'),
        contentTypeInput: document.getElementById('contentType'),
        nicheSelect: document.getElementById('nicheSelect'),
        segmentBtns: document.querySelectorAll('.segment-btn'),
        usageCheckboxes: document.querySelectorAll('input[name="usage"]'),
        
        // Outputs
        minPrice: document.getElementById('minPrice'),
        maxPrice: document.getElementById('maxPrice'),
        mobileMin: document.getElementById('mobileMin'),
        mobileMax: document.getElementById('mobileMax'),
        
        // Helpers
        expDetail: document.getElementById('expDetail'),
        
        // Actions
        generatePitchBtn: document.getElementById('generatePitchBtn'),
        downloadQuoteBtn: document.getElementById('downloadQuoteBtn'),
        themeToggle: document.getElementById('themeToggle'),
        
        // Pitch Panel
        pitchPanel: document.getElementById('pitchPanel'),
        pitchText: document.getElementById('pitchText'),
        copyPitchBtn: document.getElementById('copyPitchBtn'),
        closePitchBtn: document.querySelector('.close-pitch')
    };

    const expText = {
        'beginner': '<i class="fas fa-info-circle"></i> Best for creators building their initial portfolio.',
        'intermediate': '<i class="fas fa-check-circle"></i> For creators with consistent quality and proven ROI.',
        'pro': '<i class="fas fa-star"></i> For strategists with premium equipment and high demand.'
    };

    function init() {
        initTheme();
        initTomSelect();
        bindEvents();
        triggerCalc();
    }

    function initTheme() {
        const saved = localStorage.getItem('fairugc-theme');
        if (saved === 'dark') document.body.classList.add('dark-mode');
        
        els.themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('fairugc-theme', isDark ? 'dark' : 'light');
            els.themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }

    function initTomSelect() {
        if (els.nicheSelect) {
            new TomSelect('#nicheSelect', {
                create: false,
                sortField: { field: "text", direction: "asc" },
                onChange: (val) => { state.niche = val; triggerCalc(); }
            });
        }
    }

    function bindEvents() {
        // Content Pills
        els.pills.forEach(pill => {
            pill.addEventListener('click', () => {
                els.pills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                state.contentType = pill.dataset.value;
                els.contentTypeInput.value = state.contentType;
                triggerCalc();
            });
        });

        // Segments
        els.segmentBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                els.segmentBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.experience = btn.dataset.value;
                els.expDetail.innerHTML = expText[state.experience];
                triggerCalc();
            });
        });

        // Usage
        els.usageCheckboxes.forEach(cb => cb.addEventListener('change', triggerCalc));

        // Pitch Gen
        els.generatePitchBtn.addEventListener('click', generatePitch);
        els.closePitchBtn.addEventListener('click', () => els.pitchPanel.classList.add('hidden'));
        els.copyPitchBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(els.pitchText.value);
            els.copyPitchBtn.textContent = "Copied!";
            setTimeout(() => els.copyPitchBtn.textContent = "Copy to Clipboard", 2000);
        });

        // PDF
        els.downloadQuoteBtn.addEventListener('click', generatePDF);
    }

    function triggerCalc() {
        clearTimeout(state.timer);
        state.timer = setTimeout(calculate, config.debounceTime);
    }

    async function calculate() {
        const usage = Array.from(els.usageCheckboxes).filter(c => c.checked).map(c => c.value);
        
        try {
            const res = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content_type: state.contentType,
                    niche: state.niche,
                    experience_level: state.experience,
                    usage_rights: usage
                })
            });
            
            if (res.ok) {
                const data = await res.json();
                animateNum(els.minPrice, data.min_price);
                animateNum(els.maxPrice, data.max_price);
                if(els.mobileMin) els.mobileMin.innerText = data.min_price;
                if(els.mobileMax) els.mobileMax.innerText = data.max_price;
            }
        } catch (e) { console.error(e); }
    }

    async function generatePitch() {
        els.generatePitchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        try {
            const res = await fetch('/api/pitch/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mood: 'professional' })
            });
            if (res.ok) {
                const data = await res.json();
                // Basic formatting
                let text = data.content.replace('{brand_name}', '[Brand Name]').replace('{product_type}', 'products');
                els.pitchText.value = text;
                els.pitchPanel.classList.remove('hidden');
                els.pitchPanel.scrollIntoView({ behavior: 'smooth' });
            }
        } catch(e) { alert('Error generating pitch'); } 
        finally { els.generatePitchBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Pitch'; }
    }

    function generatePDF() {
        if (!window.jspdf) return;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        doc.setFontSize(20);
        doc.text("FairUGC Quote", 20, 20);
        doc.setFontSize(12);
        doc.text(`Estimated: $${els.minPrice.innerText} - $${els.maxPrice.innerText}`, 20, 40);
        
        doc.save("FairUGC_Quote.pdf");
    }

    function animateNum(obj, end) {
        const start = parseInt(obj.innerText.replace(/,/g, '')) || 0;
        if (start === end) return;
        const duration = 500;
        let startTime = null;
        
        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) window.requestAnimationFrame(step);
        };
        window.requestAnimationFrame(step);
    }

    init();
});