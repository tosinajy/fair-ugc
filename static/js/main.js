document.addEventListener('DOMContentLoaded', () => {
    
    const $ = window.jQuery;

    const config = { debounceTime: 300 };
    let state = {
        contentTypes: [], 
        niche: 'lifestyle',
        experience: 'beginner',
        timer: null,
        emailCaptured: false,
        currentBreakdown: null
    };

    const els = {
        pills: document.querySelectorAll('.type-pill'),
        nicheSelect: document.getElementById('nicheSelect'),
        segmentBtns: document.querySelectorAll('.segment-btn'),
        usageCheckboxes: document.querySelectorAll('input[name="usage"]'),
        
        minPrice: document.getElementById('minPrice'),
        maxPrice: document.getElementById('maxPrice'),
        mobileMin: document.getElementById('mobileMin'),
        mobileMax: document.getElementById('mobileMax'),
        
        bdBase: document.getElementById('bdBase'),
        bdTypesList: document.getElementById('bdTypesList'),
        bdNiche: document.getElementById('bdNiche'),
        bdExp: document.getElementById('bdExp'),
        bdTotal: document.getElementById('bdTotal'),
        bdUsageContainer: document.getElementById('bdUsageContainer'),
        breakdownContent: document.getElementById('breakdownContent'),
        breakdownOverlay: document.getElementById('breakdownOverlay'),
        
        modal: document.getElementById('leadModal'),
        leadForm: document.getElementById('leadForm'),
        leadEmail: document.getElementById('leadEmail'),
        modalTriggers: document.querySelectorAll('.trigger-modal'),
        
        pitchPanel: document.getElementById('pitchPanel'),
        pitchText: document.getElementById('pitchText'),
        pitchMood: document.getElementById('pitchMood'),
        generatePitchBtn: document.getElementById('generatePitchBtn'),
        mobileGeneratePitchBtn: document.getElementById('mobileGeneratePitchBtn'), 
        downloadQuoteBtn: document.getElementById('downloadQuoteBtn'),
        copyPitchBtn: document.getElementById('copyPitchBtn'),
        closePitchBtns: document.querySelectorAll('.close-pitch, #dismissPitchBtn'), 
        
        themeToggle: document.getElementById('themeToggle')
    };

    function init() {
        els.pills.forEach(p => {
            if(p.classList.contains('active')) state.contentTypes.push(p.dataset.value);
        });
        
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
                onChange: (val) => { state.niche = val; triggerCalc(); },
                render: {
                    option: function(data, escape) {
                        return '<div>' + escape(data.text) + '</div>';
                    },
                    item: function(data, escape) {
                        return '<div>' + escape(data.text) + '</div>';
                    }
                }
            });
        }
    }

    function bindEvents() {
        // Content Pills
        els.pills.forEach(pill => {
            pill.addEventListener('click', () => {
                const val = pill.dataset.value;
                if (pill.classList.contains('active')) {
                    if (state.contentTypes.length > 1) {
                        pill.classList.remove('active');
                        state.contentTypes = state.contentTypes.filter(t => t !== val);
                    }
                } else {
                    pill.classList.add('active');
                    if (!state.contentTypes.includes(val)) {
                        state.contentTypes.push(val);
                    }
                }
                triggerCalc();
            });
        });

        els.segmentBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                els.segmentBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.experience = btn.dataset.value;
                triggerCalc();
            });
        });

        els.usageCheckboxes.forEach(cb => cb.addEventListener('change', triggerCalc));

        // Pitch Generation
        els.generatePitchBtn.addEventListener('click', generatePitch);
        
        // Mobile Pitch Button Logic
        if(els.mobileGeneratePitchBtn) {
            els.mobileGeneratePitchBtn.addEventListener('click', () => {
                // Generate the pitch
                generatePitch();
                
                // Show the pitch panel (remove hidden class)
                if (els.pitchPanel) {
                    els.pitchPanel.classList.remove('hidden');
                    
                    // We need to ensure the result panel is visible on mobile for this to be seen
                    // The CSS hides .result-panel on mobile. We must override this temporarily.
                    const resultPanel = document.querySelector('.result-panel');
                    if(resultPanel) {
                        resultPanel.style.display = 'block';
                        
                        // Scroll to the pitch panel specifically
                        setTimeout(() => {
                            els.pitchPanel.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }, 100);
                    }
                }
            });
        }

        // Close Pitch Panel Logic
        els.closePitchBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                els.pitchPanel.classList.add('hidden');
                // Re-hide result panel on mobile if we forced it open
                if (window.innerWidth <= 900) {
                    const resultPanel = document.querySelector('.result-panel');
                    if(resultPanel) resultPanel.style.display = ''; // Revert to CSS
                }
            });
        });

        els.copyPitchBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(els.pitchText.value);
            els.copyPitchBtn.textContent = "Copied!";
            setTimeout(() => els.copyPitchBtn.textContent = "Copy to Clipboard", 2000);
        });

        // Modal Logic
        els.modalTriggers.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if (state.emailCaptured) {
                    if(e.target.id === 'downloadQuoteBtn') generatePDF();
                } else {
                    if ($) $(els.modal).modal('show');
                }
            });
        });

        els.leadForm.addEventListener('submit', handleLeadSubmit);
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
                    content_type: state.contentTypes, 
                    niche: state.niche,
                    experience_level: state.experience,
                    usage_rights: usage
                })
            });
            
            if (res.ok) {
                const data = await res.json();
                state.currentBreakdown = data.breakdown;
                
                const fmt = (n) => n.toLocaleString();
                
                if(els.minPrice) animateNum(els.minPrice, data.min_price);
                if(els.maxPrice) animateNum(els.maxPrice, data.max_price);
                
                // Explicitly update mobile footer numbers
                if(els.mobileMin) els.mobileMin.textContent = fmt(data.min_price);
                if(els.mobileMax) els.mobileMax.textContent = fmt(data.max_price);

                updateBreakdownUI(data.breakdown);
            }
        } catch (e) { console.error(e); }
    }

    function updateBreakdownUI(bd) {
        if(!bd) return;
        const fmt = (n) => n.toLocaleString();
        
        if(els.bdBase) els.bdBase.innerText = `$${fmt(bd.base_rate)}`;
        if(els.bdNiche) els.bdNiche.innerText = `x${bd.niche_factor}`;
        if(els.bdExp) els.bdExp.innerText = `x${bd.exp_factor}`;
        if(els.bdTotal) els.bdTotal.innerText = `$${fmt(bd.adjusted_base + bd.total_usage_cost)}`;

        if (els.bdTypesList && bd.selected_types) {
            els.bdTypesList.innerText = `Includes: ${bd.selected_types.join(', ')}`;
        }

        if(els.bdUsageContainer) {
            els.bdUsageContainer.innerHTML = '';
            if (bd.usage_items && bd.usage_items.length > 0) {
                bd.usage_items.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'breakdown-row sub';
                    div.innerHTML = `<span>+ ${item.name} (${Math.round(item.rate*100)}%)</span><span>$${fmt(item.cost)}</span>`;
                    els.bdUsageContainer.appendChild(div);
                });
            } else {
                const div = document.createElement('div');
                div.className = 'breakdown-row sub';
                div.innerHTML = `<span>No Usage Rights</span><span>$0</span>`;
                els.bdUsageContainer.appendChild(div);
            }
        }
    }

    async function handleLeadSubmit(e) {
        e.preventDefault();
        const email = els.leadEmail.value;
        const btn = document.getElementById('submitLeadBtn');
        
        btn.classList.add('loading');

        try {
            const res = await fetch('/api/lead', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });

            if (res.ok) {
                state.emailCaptured = true;
                if ($) $(els.modal).modal('hide');
                
                els.breakdownContent.classList.remove('blur-content');
                els.breakdownOverlay.style.opacity = '0';
                setTimeout(() => els.breakdownOverlay.style.display = 'none', 300);
                els.downloadQuoteBtn.innerHTML = '<i class="fas fa-file-pdf"></i> Download PDF';
                setTimeout(generatePDF, 500);
            } else {
                alert("Please enter a valid email.");
            }
        } catch(err) {
            console.error(err);
        } finally {
            btn.classList.remove('loading');
        }
    }

    async function generatePitch() {
        if(els.generatePitchBtn) els.generatePitchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        const selectedMood = els.pitchMood ? (els.pitchMood.value || 'professional') : 'professional';
        
        try {
            const res = await fetch('/api/pitch/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    mood: selectedMood,
                    niche: state.niche 
                })
            });
            if (res.ok) {
                const data = await res.json();
                let text = data.content.replace('{brand_name}', '[Brand Name]');
                if(els.pitchText) els.pitchText.value = text;
                if(els.pitchPanel) {
                    els.pitchPanel.classList.remove('hidden');
                    els.pitchPanel.scrollIntoView({ behavior: 'smooth' });
                }
            }
        } catch(e) { alert('Error generating pitch'); } 
        finally { if(els.generatePitchBtn) els.generatePitchBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Pitch'; }
    }

    function generatePDF() {
        if (!state.emailCaptured) {
            if ($) $(els.modal).modal('show');
            return;
        }

        if (!window.jspdf) return;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const bd = state.currentBreakdown;
        
        doc.setFillColor(79, 70, 229); 
        doc.rect(0, 0, 210, 45, 'F');
        
        const logoImg = new Image();
        logoImg.src = '/static/fair-ugc.png';
        logoImg.onload = function() {
            doc.addImage(logoImg, 'PNG', 15, 12, 20, 20);
            finishPDF(doc, bd);
        };
        logoImg.onerror = function() {
            finishPDF(doc, bd);
        };
    }

    function finishPDF(doc, bd) {
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(24);
        doc.setFont("helvetica", "bold");
        doc.text("FairUGC Quote", 42, 22);
        
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        doc.text("Professional Creator Estimation", 42, 28);
        doc.text(`Date: ${new Date().toLocaleDateString()}`, 160, 28);

        let y = 65;

        doc.setDrawColor(200, 200, 200);
        doc.setFillColor(248, 250, 252);
        doc.rect(15, 55, 180, 50, 'FD');

        doc.setTextColor(50, 50, 50);
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.text("Project Scope", 22, 68);

        doc.setFontSize(11);
        doc.setFont("helvetica", "normal");
        
        const typeStr = bd.selected_types ? bd.selected_types.join(', ') : 'Mixed Bundle';
        doc.text("Content Types:", 22, 80);
        doc.setFont("helvetica", "bold");
        doc.text(typeStr, 60, 80);
        
        doc.setFont("helvetica", "normal");
        doc.text("Niche:", 22, 90);
        doc.setFont("helvetica", "bold");
        doc.text(state.niche.toUpperCase(), 60, 90);

        doc.setFont("helvetica", "normal");
        doc.text("Experience:", 22, 100);
        doc.setFont("helvetica", "bold");
        doc.text(state.experience.toUpperCase(), 60, 100);

        y = 125;

        doc.setTextColor(50, 50, 50);
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.text("Cost Breakdown", 15, y);
        y += 10;

        doc.setLineWidth(0.5);
        doc.line(15, y, 195, y);
        y += 15;

        const fmt = (n) => n.toLocaleString();

        doc.setFontSize(12);
        doc.setFont("helvetica", "normal");
        doc.text("Base Rate (Content Production)", 15, y);
        doc.text(`$${fmt(bd.base_rate)}`, 170, y, { align: "right" });
        y += 10;

        doc.setTextColor(100, 100, 100);
        doc.setFontSize(10);
        doc.text(`Experience Multiplier (x${bd.exp_factor})`, 15, y);
        y += 6;
        doc.text(`Niche Multiplier (x${bd.niche_factor})`, 15, y);
        y += 10;

        doc.setTextColor(50, 50, 50);
        doc.setFontSize(12);
        if (bd.usage_items && bd.usage_items.length > 0) {
            bd.usage_items.forEach(item => {
                doc.text(`+ ${item.name}`, 15, y);
                doc.text(`$${fmt(item.cost)}`, 170, y, { align: "right" });
                y += 8;
            });
        } else {
            doc.text("Usage Rights: Standard Organic Only", 15, y);
            doc.text("$0", 170, y, { align: "right" });
            y += 8;
        }

        y += 5;
        doc.line(15, y, 195, y);
        y += 20;

        doc.setFillColor(240, 245, 255);
        doc.setDrawColor(79, 70, 229);
        doc.rect(120, y-15, 75, 25, 'FD');

        doc.setFontSize(16);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(79, 70, 229);
        doc.text("TOTAL:", 125, y+2);
        doc.text(`$${fmt(bd.adjusted_base + bd.total_usage_cost)}`, 188, y+2, { align: "right" });

        doc.setFontSize(9);
        doc.setTextColor(150, 150, 150);
        doc.setFont("helvetica", "normal");
        const pageHeight = doc.internal.pageSize.height;
        doc.text("Generated by FairUGC - FairUGC.com", 105, pageHeight - 10, { align: "center" });

        doc.save("FairUGC_Quote.pdf");
    }

    function animateNum(obj, end) {
        if (!obj) return;
        const start = parseInt(obj.innerText.replace(/,/g, '').replace('$', '')) || 0;
        if (start === end) return;
        const duration = 500;
        let startTime = null;
        
        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const val = Math.floor(progress * (end - start) + start);
            obj.innerHTML = val.toLocaleString(); // Add commas
            if (progress < 1) window.requestAnimationFrame(step);
        };
        window.requestAnimationFrame(step);
    }

    init();
});