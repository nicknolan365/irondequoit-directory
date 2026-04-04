// Irondequoit Directory — Client-Side Search
(function() {
  let searchData = [];
  let searchInput, searchResults;

  // Load search index
  async function loadSearchIndex() {
    try {
      const resp = await fetch('/search-index.json');
      searchData = await resp.json();
    } catch (e) {
      console.error('Failed to load search index:', e);
    }
  }

  function init() {
    searchInput = document.getElementById('search-input');
    searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) return;

    loadSearchIndex();

    searchInput.addEventListener('input', debounce(handleSearch, 200));
    searchInput.addEventListener('focus', () => {
      if (searchInput.value.trim().length >= 2) handleSearch();
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#search-container')) {
        searchResults.classList.remove('active');
      }
    });

    // Keyboard nav
    searchInput.addEventListener('keydown', (e) => {
      const items = searchResults.querySelectorAll('.search-result-item');
      const active = searchResults.querySelector('.search-result-item.active-item');
      let idx = Array.from(items).indexOf(active);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (idx < items.length - 1) idx++;
        else idx = 0;
        items.forEach(i => i.classList.remove('active-item'));
        items[idx]?.classList.add('active-item');
        items[idx]?.scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (idx > 0) idx--;
        else idx = items.length - 1;
        items.forEach(i => i.classList.remove('active-item'));
        items[idx]?.classList.add('active-item');
        items[idx]?.scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (active) {
          window.location.href = active.dataset.url;
        }
      } else if (e.key === 'Escape') {
        searchResults.classList.remove('active');
      }
    });
  }

  function handleSearch() {
    const query = searchInput.value.trim().toLowerCase();

    if (query.length < 2) {
      searchResults.classList.remove('active');
      return;
    }

    const results = searchData.filter(item => {
      const fields = [
        item.title,
        item.tagline,
        item.category,
        item.subcategory,
        item.address,
        item.description
      ].join(' ').toLowerCase();

      // All query words must match
      const words = query.split(/\s+/);
      return words.every(word => fields.includes(word));
    });

    // Sort: premium first, then alphabetical
    results.sort((a, b) => {
      if (a.premium && !b.premium) return -1;
      if (!a.premium && b.premium) return 1;
      return a.title.localeCompare(b.title);
    });

    renderResults(results.slice(0, 8));
  }

  function renderResults(results) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-no-results">No businesses found. Try a different search.</div>';
      searchResults.classList.add('active');
      return;
    }

    searchResults.innerHTML = results.map(r => `
      <div class="search-result-item" data-url="${r.url}" onclick="window.location.href='${r.url}'">
        <div>
          <div class="search-result-name">
            ${r.premium ? '⭐ ' : ''}${escapeHtml(r.title)}
          </div>
          <div class="search-result-meta">
            ${escapeHtml(r.subcategory)} · ${escapeHtml(r.category)}
          </div>
        </div>
      </div>
    `).join('');

    searchResults.classList.add('active');
  }

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function debounce(fn, delay) {
    let timer;
    return function(...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  // Init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
