/* =============================================================================
   ITSERR-RESILIENCE Corpus Browser — Application Logic
   ============================================================================= */

(function () {
  'use strict';

  // State
  let corpus = null;
  let activeChapterId = null;
  let activeFilters = new Set(['biblical', 'patristic', 'reformation', 'classical', 'confessional']);
  let activeEpistemicFilters = new Set(['FACTUAL', 'INTERPRETIVE']);
  let searchQuery = '';

  // DOM references (assigned after DOMContentLoaded)
  let sidebarNav, contentArea, searchInput, searchCount, tooltip;

  // ============================================================================
  // DATA LOADING
  // ============================================================================

  async function loadCorpus() {
    try {
      const resp = await fetch('data/corpus.json');
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      corpus = await resp.json();
      init();
    } catch (err) {
      contentArea.innerHTML = `
        <div class="no-results">
          <h3>Failed to load corpus data</h3>
          <p>${err.message}</p>
          <p style="margin-top:12px;font-size:12px;">Make sure <code>data/corpus.json</code> exists. Run <code>build_corpus_json.py</code> to generate it.</p>
        </div>`;
    }
  }

  // ============================================================================
  // INITIALIZATION
  // ============================================================================

  function init() {
    renderSidebar();
    renderStats();
    renderFilters();
    renderWelcome();
    bindEvents();
  }

  // ============================================================================
  // SIDEBAR
  // ============================================================================

  function renderSidebar() {
    let html = '';
    for (const ch of corpus.chapters) {
      const refCount = ch.pages.reduce((sum, p) => sum + p.references.length, 0);
      const pageRange = `pp. ${ch.start_page}–${ch.end_page}`;

      html += `
        <div class="chapter-group" data-chapter="${ch.id}">
          <div class="chapter-item" data-chapter="${ch.id}">
            <span class="expand-icon">&#9654;</span>
            <span class="chapter-title">${ch.title}</span>
            <span class="chapter-meta">${pageRange}</span>
          </div>
          <div class="page-list">`;

      for (const pg of ch.pages) {
        const pgRefs = pg.references.length;
        const refBadge = pgRefs > 0 ? ` (${pgRefs})` : '';
        html += `<div class="page-item" data-page="${pg.page}" data-chapter="${ch.id}">p. ${pg.page}${refBadge}</div>`;
      }

      html += `</div></div>`;
    }
    sidebarNav.innerHTML = html;
  }

  function renderStats() {
    const statsPanel = document.querySelector('.stats-panel');
    if (!statsPanel || !corpus) return;

    const types = corpus.entity_types;
    let html = '<h3>Detected References</h3>';
    for (const t of types) {
      const count = corpus.stats.by_type[t.id] || 0;
      if (count > 0) {
        html += `
          <div class="stat-row">
            <span class="stat-label"><span class="stat-dot" style="background:${t.color}"></span>${t.label}</span>
            <span class="stat-value">${count}</span>
          </div>`;
      }
    }
    html += `
      <div class="stat-row" style="margin-top:8px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.08)">
        <span class="stat-label">Total</span>
        <span class="stat-value">${corpus.stats.total_references}</span>
      </div>`;
    statsPanel.innerHTML = html;
  }

  // ============================================================================
  // FILTERS
  // ============================================================================

  function renderFilters() {
    const filterBar = document.querySelector('.filter-bar');
    if (!filterBar || !corpus) return;

    let html = '<span class="filter-label">Entity type</span>';

    for (const t of corpus.entity_types) {
      const count = corpus.stats.by_type[t.id] || 0;
      if (count > 0) {
        const isActive = activeFilters.has(t.id);
        html += `<span class="filter-tag ${isActive ? 'active' : ''}" data-type="${t.id}"><span class="dot"></span>${t.label} (${count})</span>`;
      }
    }

    html += '<span class="filter-separator"></span><span class="filter-label">Confidence</span>';

    for (const e of corpus.epistemic_types) {
      const count = corpus.stats.by_epistemic[e.id] || 0;
      if (count > 0) {
        const isActive = activeEpistemicFilters.has(e.id);
        html += `<span class="filter-tag epistemic ${isActive ? 'active' : ''}" data-epistemic="${e.id}"><span class="dot"></span>${e.label} (${count})</span>`;
      }
    }

    filterBar.innerHTML = html;
  }

  // ============================================================================
  // CONTENT RENDERING
  // ============================================================================

  function renderWelcome() {
    contentArea.innerHTML = `
      <div class="info-banner">
        <h2>ITSERR-RESILIENCE Corpus Browser</h2>
        <p>Exploring annotated 16th-century theological texts from the Kingdom of Hungary.</p>
        <p>This prototype demonstrates <strong>rule-based entity detection</strong> (Stage 4, Layer 1 of the GNORM adaptation pipeline) applied to Leonard Stöckel's <em>Annotationes in Locos communes</em> (1561).</p>
        <p style="margin-top:8px">
          <span class="badge">Layer 1 — Rule-based detection</span>
          <span class="badge" style="margin-left:4px">Pre-CRF prototype</span>
        </p>
      </div>
      <div class="welcome-screen">
        <h2>Select a chapter to begin</h2>
        <p>Choose a chapter from the sidebar to browse the annotated text. Detected references are highlighted with color-coded annotations. Use the search bar to find specific terms across the corpus.</p>
      </div>`;
  }

  function renderChapter(chapterId) {
    activeChapterId = chapterId;

    const ch = corpus.chapters.find(c => c.id === chapterId);
    if (!ch) return;

    // Update sidebar
    document.querySelectorAll('.chapter-item').forEach(el => {
      el.classList.toggle('active', el.dataset.chapter === chapterId);
      el.classList.toggle('expanded', el.dataset.chapter === chapterId);
    });
    document.querySelectorAll('.page-list').forEach(el => {
      el.classList.toggle('visible', el.parentElement.dataset.chapter === chapterId);
    });

    // Compute filtered ref counts
    const refCounts = {};
    for (const pg of ch.pages) {
      for (const ref of pg.references) {
        if (activeFilters.has(ref.type) && activeEpistemicFilters.has(ref.epistemic)) {
          refCounts[ref.type] = (refCounts[ref.type] || 0) + 1;
        }
      }
    }

    let statsHtml = '';
    for (const [type, count] of Object.entries(refCounts)) {
      const entityType = corpus.entity_types.find(t => t.id === type);
      if (entityType) {
        statsHtml += `<span class="stat"><span class="dot" style="background:${entityType.color}"></span>${entityType.label}: ${count}</span>`;
      }
    }

    let html = `
      <div class="chapter-header">
        <h2>${ch.title}</h2>
        <div class="chapter-en">${ch.title_en} — Pages ${ch.start_page}–${ch.end_page}</div>
        <div class="chapter-stats">${statsHtml}</div>
      </div>`;

    if (ch.pages.length === 0) {
      html += '<div class="no-results">No content available for this chapter.</div>';
    } else {
      for (const pg of ch.pages) {
        html += renderPage(pg);
      }
    }

    contentArea.innerHTML = html;
    contentArea.scrollTop = 0;
  }

  function renderPage(pg) {
    const annotatedText = applyAnnotations(pg.text, pg.references);

    return `
      <div class="page-block" id="page-${pg.page}">
        <div class="page-label">Page ${pg.page}</div>
        <div class="text-content">${annotatedText}</div>
      </div>`;
  }

  function applyAnnotations(text, references) {
    // Filter references by active filters
    const filteredRefs = references.filter(
      r => activeFilters.has(r.type) && activeEpistemicFilters.has(r.epistemic)
    );

    if (filteredRefs.length === 0 && !searchQuery) {
      return escapeHtml(text);
    }

    // Build sorted list of insertion points
    const insertions = [];

    for (const ref of filteredRefs) {
      // Find the reference text position in the text
      const idx = text.indexOf(ref.text, Math.max(0, ref.start - 10));
      if (idx === -1) continue;

      insertions.push({
        pos: idx,
        end: idx + ref.text.length,
        type: 'ref-open',
        ref: ref,
      });
      insertions.push({
        pos: idx + ref.text.length,
        end: idx + ref.text.length,
        type: 'ref-close',
        ref: ref,
      });
    }

    // Apply search highlights if query exists
    if (searchQuery && searchQuery.length >= 2) {
      const regex = new RegExp(escapeRegex(searchQuery), 'gi');
      let match;
      while ((match = regex.exec(text)) !== null) {
        insertions.push({
          pos: match.index,
          end: match.index + match[0].length,
          type: 'search-open',
        });
        insertions.push({
          pos: match.index + match[0].length,
          end: match.index + match[0].length,
          type: 'search-close',
        });
      }
    }

    // Sort: position ascending, closes before opens at same position
    insertions.sort((a, b) => {
      if (a.pos !== b.pos) return a.pos - b.pos;
      // Close tags before open tags at same position
      const aOrder = a.type.includes('close') ? 0 : 1;
      const bOrder = b.type.includes('close') ? 0 : 1;
      return aOrder - bOrder;
    });

    // Build output
    let result = '';
    let lastIdx = 0;

    for (const ins of insertions) {
      // Add text before this insertion
      if (ins.pos > lastIdx) {
        result += escapeHtml(text.slice(lastIdx, ins.pos));
      }

      if (ins.type === 'ref-open') {
        const r = ins.ref;
        result += `<span class="ref-highlight" data-type="${r.type}" data-confidence="${r.confidence}" data-epistemic="${r.epistemic}" data-text="${escapeAttr(r.text)}" data-method="${r.method}">`;
      } else if (ins.type === 'ref-close') {
        result += '</span>';
      } else if (ins.type === 'search-open') {
        result += '<span class="search-highlight">';
      } else if (ins.type === 'search-close') {
        result += '</span>';
      }

      lastIdx = ins.pos;
    }

    // Add remaining text
    if (lastIdx < text.length) {
      result += escapeHtml(text.slice(lastIdx));
    }

    return result;
  }

  // ============================================================================
  // SEARCH
  // ============================================================================

  function performSearch(query) {
    searchQuery = query.trim();

    if (!searchQuery || searchQuery.length < 2) {
      searchCount.textContent = '';
      if (activeChapterId) {
        renderChapter(activeChapterId);
      }
      return;
    }

    // Count matches across all chapters
    const regex = new RegExp(escapeRegex(searchQuery), 'gi');
    let totalMatches = 0;
    const chapterMatches = [];

    for (const ch of corpus.chapters) {
      let chMatches = 0;
      for (const pg of ch.pages) {
        const matches = pg.text.match(regex);
        if (matches) chMatches += matches.length;
      }
      if (chMatches > 0) {
        totalMatches += chMatches;
        chapterMatches.push({ chapter: ch, count: chMatches });
      }
    }

    searchCount.textContent = totalMatches > 0
      ? `${totalMatches} match${totalMatches !== 1 ? 'es' : ''} in ${chapterMatches.length} chapter${chapterMatches.length !== 1 ? 's' : ''}`
      : 'No matches';

    // If viewing a chapter, re-render to show highlights
    if (activeChapterId) {
      renderChapter(activeChapterId);
    } else if (chapterMatches.length > 0) {
      // Show search results overview
      renderSearchResults(chapterMatches, totalMatches);
    }
  }

  function renderSearchResults(chapterMatches, totalMatches) {
    let html = `
      <div class="info-banner">
        <h2>Search Results: "${escapeHtml(searchQuery)}"</h2>
        <p>${totalMatches} matches found across ${chapterMatches.length} chapters. Click a chapter to view the matches in context.</p>
      </div>`;

    for (const { chapter, count } of chapterMatches) {
      html += `
        <div class="page-block" style="cursor:pointer" onclick="document.querySelector('[data-chapter=${chapter.id}] .chapter-item').click()">
          <div class="page-label">${chapter.title} — ${chapter.title_en} (${count} matches)</div>
        </div>`;
    }

    contentArea.innerHTML = html;
  }

  // ============================================================================
  // TOOLTIP
  // ============================================================================

  function showTooltip(el, x, y) {
    const type = el.dataset.type;
    const confidence = el.dataset.confidence;
    const epistemic = el.dataset.epistemic;
    const text = el.dataset.text;
    const method = el.dataset.method;

    const entityType = corpus.entity_types.find(t => t.id === type);
    const typeLabel = entityType ? entityType.label : type;
    const typeColor = entityType ? entityType.color : '#999';

    const epistemicClass = epistemic === 'FACTUAL' ? 'factual' : 'interpretive';

    tooltip.innerHTML = `
      <div class="tooltip-type" style="color:${typeColor}">${typeLabel}</div>
      <div class="tooltip-text">"${text}"</div>
      <div class="tooltip-meta">
        <span class="tooltip-badge ${epistemicClass}">${epistemic}</span>
        <span style="opacity:0.6;font-size:10px">Confidence: ${Math.round(confidence * 100)}%</span>
      </div>
      <div style="margin-top:4px;font-size:10px;opacity:0.5">Detection: ${method}</div>`;

    // Position tooltip
    const rect = tooltip.getBoundingClientRect();
    const maxX = window.innerWidth - 300;
    const maxY = window.innerHeight - 120;

    tooltip.style.left = Math.min(x + 12, maxX) + 'px';
    tooltip.style.top = Math.min(y + 12, maxY) + 'px';
    tooltip.classList.add('visible');
  }

  function hideTooltip() {
    tooltip.classList.remove('visible');
  }

  // ============================================================================
  // EVENTS
  // ============================================================================

  function bindEvents() {
    // Chapter clicks
    sidebarNav.addEventListener('click', function (e) {
      const chapterItem = e.target.closest('.chapter-item');
      const pageItem = e.target.closest('.page-item');

      if (chapterItem) {
        const chId = chapterItem.dataset.chapter;
        renderChapter(chId);
      } else if (pageItem) {
        const chId = pageItem.dataset.chapter;
        const pageNum = pageItem.dataset.page;
        if (activeChapterId !== chId) {
          renderChapter(chId);
        }
        // Scroll to page
        setTimeout(() => {
          const pageEl = document.getElementById(`page-${pageNum}`);
          if (pageEl) {
            pageEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Mark active
            document.querySelectorAll('.page-item').forEach(el => el.classList.remove('active'));
            pageItem.classList.add('active');
          }
        }, 50);
      }
    });

    // Search
    let searchTimeout;
    searchInput.addEventListener('input', function () {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => performSearch(this.value), 250);
    });

    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        this.value = '';
        performSearch('');
      }
    });

    // Filter toggles
    document.querySelector('.filter-bar').addEventListener('click', function (e) {
      const tag = e.target.closest('.filter-tag');
      if (!tag) return;

      if (tag.classList.contains('epistemic')) {
        const eid = tag.dataset.epistemic;
        if (activeEpistemicFilters.has(eid)) {
          if (activeEpistemicFilters.size > 1) activeEpistemicFilters.delete(eid);
        } else {
          activeEpistemicFilters.add(eid);
        }
      } else {
        const tid = tag.dataset.type;
        if (activeFilters.has(tid)) {
          if (activeFilters.size > 1) activeFilters.delete(tid);
        } else {
          activeFilters.add(tid);
        }
      }

      renderFilters();
      if (activeChapterId) renderChapter(activeChapterId);
    });

    // Tooltip on hover
    contentArea.addEventListener('mouseover', function (e) {
      const ref = e.target.closest('.ref-highlight');
      if (ref) {
        showTooltip(ref, e.clientX, e.clientY);
      }
    });

    contentArea.addEventListener('mousemove', function (e) {
      const ref = e.target.closest('.ref-highlight');
      if (ref && tooltip.classList.contains('visible')) {
        const maxX = window.innerWidth - 300;
        const maxY = window.innerHeight - 120;
        tooltip.style.left = Math.min(e.clientX + 12, maxX) + 'px';
        tooltip.style.top = Math.min(e.clientY + 12, maxY) + 'px';
      }
    });

    contentArea.addEventListener('mouseout', function (e) {
      const ref = e.target.closest('.ref-highlight');
      if (ref) {
        hideTooltip();
      }
    });
  }

  // ============================================================================
  // HELPERS
  // ============================================================================

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function escapeAttr(str) {
    return str.replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // ============================================================================
  // BOOT
  // ============================================================================

  document.addEventListener('DOMContentLoaded', function () {
    sidebarNav = document.querySelector('.sidebar-nav');
    contentArea = document.querySelector('.content-area');
    searchInput = document.querySelector('.search-box input');
    searchCount = document.querySelector('.search-results-count');
    tooltip = document.querySelector('.ref-tooltip');

    loadCorpus();
  });
})();
