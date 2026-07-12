(function initDictCoverLightboxModule() {
  function openLightbox(lightbox, imgEl, src, alt) {
    imgEl.src = src;
    imgEl.alt = alt || 'Dictionary cover';
    lightbox.classList.add('active');
    document.body.classList.add('dict-cover-lightbox-open');
  }

  function closeLightbox(lightbox) {
    lightbox.classList.remove('active');
    document.body.classList.remove('dict-cover-lightbox-open');
  }

  function setup() {
    const previews = document.querySelectorAll('.dict-cover-preview');
    if (!previews.length) return;

    let lightbox = document.getElementById('dict-cover-lightbox');
    if (!lightbox) {
      lightbox = document.createElement('div');
      lightbox.id = 'dict-cover-lightbox';
      lightbox.className = 'dict-cover-lightbox';
      lightbox.innerHTML = `
        <button type="button" class="dict-cover-lightbox-back classic-btn secondary">← Back</button>
        <div class="dict-cover-lightbox-stage">
          <img src="" alt="">
        </div>
      `;
      document.body.appendChild(lightbox);
    }

    const imgEl = lightbox.querySelector('img');
    const backBtn = lightbox.querySelector('.dict-cover-lightbox-back');

    previews.forEach((preview) => {
      preview.addEventListener('click', () => {
        openLightbox(lightbox, imgEl, preview.src, preview.alt);
      });
    });

    backBtn.addEventListener('click', (event) => {
      event.stopPropagation();
      closeLightbox(lightbox);
    });

    lightbox.addEventListener('click', (event) => {
      if (event.target === lightbox || event.target.classList.contains('dict-cover-lightbox-stage')) {
        closeLightbox(lightbox);
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox(lightbox);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
})();
