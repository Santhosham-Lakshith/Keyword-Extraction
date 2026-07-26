// ── Live text stats ────────────────────────────────────────────────────────
const textarea = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const wordCount = document.getElementById('wordCount');

function updateStats() {
  const text = textarea.value;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  charCount.textContent = `${text.length.toLocaleString()} chars`;
  wordCount.textContent = `${words.toLocaleString()} words`;
}

if (textarea) {
  textarea.addEventListener('input', updateStats);
  updateStats(); // run on page load if text is pre-filled
}

// ── Submit loading state ────────────────────────────────────────────────────
const form = document.getElementById('extractForm');
const submitBtn = document.getElementById('submitBtn');

if (form) {
  form.addEventListener('submit', () => {
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
  });
}

// ── Smooth scroll to results on load if results present ───────────────────
const results = document.getElementById('results');
if (results) {
  setTimeout(() => {
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 300);
}

// ── Copy tag on click ──────────────────────────────────────────────────────
document.querySelectorAll('.tag').forEach(tag => {
  tag.addEventListener('click', () => {
    navigator.clipboard?.writeText(tag.textContent.trim()).then(() => {
      const orig = tag.textContent;
      tag.textContent = '✓ copied';
      setTimeout(() => { tag.textContent = orig; }, 1200);
    });
  });
});

// ── Copy code blocks on click ──────────────────────────────────────────────
document.querySelectorAll('.code-block').forEach(block => {
  block.style.cursor = 'pointer';
  block.title = 'Click to copy';
  block.addEventListener('click', () => {
    navigator.clipboard?.writeText(block.textContent.trim()).then(() => {
      const orig = block.style.borderColor;
      block.style.borderColor = 'var(--accent)';
      setTimeout(() => { block.style.borderColor = orig; }, 800);
    });
  });
});
