
(function(){
  'use strict';
  var I18N = window.I18N || {};
  var INDEX = window.SEARCH_INDEX || [];
  var STORAGE_KEY = 'vmqtg_lang';
  var DEFAULT = 'vi';

  // ─── helpers ────────────────────────────────────────────────────────────
  function stripDiacritics(s){
    return (s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  }
  function getLang(){
    var saved = localStorage.getItem(STORAGE_KEY);
    if(saved && (saved==='vi'||saved==='en'||saved==='fr')) return saved;
    var nav = (navigator.language||'').slice(0,2).toLowerCase();
    if(nav==='en'||nav==='fr') return nav;
    return DEFAULT;
  }
  function setLang(lang){
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.setAttribute('lang', lang);
  }
  function lookup(key, lang){
    var entry = I18N[key];
    if(!entry) return null;
    return entry[lang] || null;
  }

  // ─── i18n apply ─────────────────────────────────────────────────────────
  function applyI18n(lang){
    // text nodes
    var nodes = document.querySelectorAll('[data-i18n]');
    nodes.forEach(function(el){
      var key = el.getAttribute('data-i18n');
      // store original VI text once
      if(!el.hasAttribute('data-vi-text')) el.setAttribute('data-vi-text', el.textContent);
      var txt = (lang==='vi') ? el.getAttribute('data-vi-text') : lookup(key, lang);
      el.textContent = txt || el.getAttribute('data-vi-text');
    });
    // html nodes
    var htmlNodes = document.querySelectorAll('[data-i18n-html]');
    htmlNodes.forEach(function(el){
      var key = el.getAttribute('data-i18n-html');
      if(!el.hasAttribute('data-vi-html')) el.setAttribute('data-vi-html', el.innerHTML);
      var html = (lang==='vi') ? el.getAttribute('data-vi-html') : lookup(key, lang);
      el.innerHTML = html || el.getAttribute('data-vi-html');
    });
    // attribute swaps: data-i18n-attr="placeholder:ui.search_ph"
    var attrNodes = document.querySelectorAll('[data-i18n-attr]');
    attrNodes.forEach(function(el){
      var spec = el.getAttribute('data-i18n-attr');
      spec.split(',').forEach(function(pair){
        var parts = pair.trim().split(':');
        var attr = parts[0], key = parts[1];
        var orig = el.getAttribute('data-vi-attr-'+attr);
        if(orig===null){ el.setAttribute('data-vi-attr-'+attr, el.getAttribute(attr)||''); orig = el.getAttribute(attr)||''; }
        var v = (lang==='vi') ? orig : lookup(key, lang);
        el.setAttribute(attr, v || orig);
      });
    });
    // update active button
    document.querySelectorAll('.lang-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-lang')===lang);
    });
    // update <title> by extracting current page title text node
    var h1 = document.querySelector('.page-title, .hero-title');
    if(h1){
      var t = h1.textContent.trim();
      if(t) document.title = t + ' — ' + (lookup('ui.site_name', lang) || 'Văn Miếu Quốc Tử Giám');
    }
  }

  // Index translatable elements into 2 regions for staggered animation.
  // Sets CSS var --i so .lang-entering rules can offset animation-delay.
  // Re-run after every applyI18n() because innerHTML swap creates new children.
  // Menu indexing: only top-level nav bar items get a stagger index.
  // Content sections use static delays in CSS (per parent section), so no
  // JS indexing is needed there — only text animates, never images/bg.
  var MENU_SEL = '.site-header [data-i18n]:not(.dropdown [data-i18n])';
  function indexElements(){
    document.querySelectorAll(MENU_SEL).forEach(function(el,i){
      el.style.setProperty('--i', i);
    });
  }

  function transitionLang(lang){
    applyI18n(lang);
    indexElements();
    // toggle .lang-entering off→on to restart animation; force reflow between
    document.body.classList.remove('lang-entering');
    void document.body.offsetWidth;
    document.body.classList.add('lang-entering');
    setTimeout(function(){
      document.body.classList.remove('lang-entering');
    }, 900);
    setLang(lang);
  }

  // ─── search ─────────────────────────────────────────────────────────────
  function highlight(text, query){
    if(!query) return text;
    var q = stripDiacritics(query);
    var src = stripDiacritics(text);
    var i = src.indexOf(q);
    if(i<0) return text;
    return text.slice(0,i)+'<mark>'+text.slice(i,i+q.length)+'</mark>'+text.slice(i+q.length);
  }
  function score(entry, query, lang){
    var q = stripDiacritics(query);
    if(!q) return 0;
    var fields = [entry[lang]||'', entry.vi||'', entry.en||'', entry.fr||'',
                  entry['sub_'+lang]||'', entry.sub_vi||''];
    var best = -1, hit=0;
    for(var i=0;i<fields.length;i++){
      var s = stripDiacritics(fields[i]);
      var idx = s.indexOf(q);
      if(idx>=0){
        hit = 1;
        // weight: earlier match + primary lang first = better
        var w = (i===0?100:i===1?80:50) - idx;
        if(w>best) best=w;
      }
    }
    return hit ? best : -1;
  }
  function runSearch(query, lang){
    if(!query.trim()) return [];
    var ranked = [];
    INDEX.forEach(function(e){
      var s = score(e, query, lang);
      if(s>=0) ranked.push({e:e, s:s});
    });
    ranked.sort(function(a,b){return b.s-a.s});
    return ranked.slice(0,10).map(function(x){return x.e});
  }
  function renderResults(results, query, lang){
    var box = document.getElementById('search-results');
    if(!box) return;
    if(!results.length){
      box.innerHTML = '<div class="search-empty">'+(lookup('ui.search_no',lang)||'Không có kết quả')+'</div>';
      box.classList.add('open'); return;
    }
    // build URL prefix from current depth
    var depth = (location.pathname.match(/\//g)||[]).length - 1;
    // Better: count slashes after the site root. Use relative trick:
    // figure out how many "../" we need by finding base of href in <link rel=stylesheet>
    var css = document.querySelector('link[rel=stylesheet]');
    var prefix = '';
    if(css){
      var href = css.getAttribute('href')||'';
      var m = href.match(/^((?:\.\.\/)+)/);
      if(m) prefix = m[1];
    }
    var html = results.map(function(r){
      var title = r[lang] || r.vi;
      var sub = r['sub_'+lang] || r.sub_vi || '';
      var url = prefix + r.url;
      return '<a class="search-result" href="'+url+'">'+
             '<span class="sr-id">'+r.id+'</span>'+
             '<span class="sr-title">'+highlight(title, query)+'</span>'+
             (sub?'<span class="sr-sub">'+highlight(sub, query)+'</span>':'')+
             '</a>';
    }).join('');
    box.innerHTML = html;
    box.classList.add('open');
  }

  // ─── init ───────────────────────────────────────────────────────────────
  function init(){
    var lang = getLang();
    setLang(lang);
    applyI18n(lang);
    indexElements();

    document.querySelectorAll('.lang-btn').forEach(function(b){
      b.addEventListener('click', function(){
        var l = b.getAttribute('data-lang');
        if(l===getLang()) return;
        transitionLang(l);
      });
    });

    var input = document.getElementById('site-search');
    var box = document.getElementById('search-results');
    if(input){
      var debounce;
      input.addEventListener('input', function(){
        clearTimeout(debounce);
        debounce = setTimeout(function(){
          var q = input.value;
          if(!q.trim()){ box.classList.remove('open'); box.innerHTML=''; return; }
          renderResults(runSearch(q, getLang()), q, getLang());
        }, 80);
      });
      input.addEventListener('focus', function(){
        if(input.value.trim()) box.classList.add('open');
      });
      document.addEventListener('click', function(e){
        if(!e.target.closest('.search-wrap')) box.classList.remove('open');
      });
      // keyboard
      input.addEventListener('keydown', function(e){
        var items = box.querySelectorAll('.search-result');
        if(!items.length) return;
        var sel = box.querySelector('.search-result.selected');
        var idx = sel ? Array.prototype.indexOf.call(items, sel) : -1;
        if(e.key==='ArrowDown'){ e.preventDefault(); idx=(idx+1)%items.length; }
        else if(e.key==='ArrowUp'){ e.preventDefault(); idx=(idx-1+items.length)%items.length; }
        else if(e.key==='Enter' && sel){ e.preventDefault(); window.location.href = sel.getAttribute('href'); return; }
        else if(e.key==='Escape'){ box.classList.remove('open'); input.blur(); return; }
        else return;
        items.forEach(function(i){i.classList.remove('selected')});
        if(items[idx]) items[idx].classList.add('selected');
      });
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // Page transitions are pure CSS (.18s fade-in on content area only).
  // No JS interceptor — browser navigates instantly, new page paints fast.

  // ─── broken-image → placeholder (capture phase: img errors don't bubble) ──
  // Re-points the failed <img> to the bundled Văn Miếu placeholder photo
  // (resolved relative to the stylesheet path so depth doesn't matter).
  document.addEventListener('error', function(e){
    var t = e.target;
    if(!t || t.tagName !== 'IMG') return;
    if(t.dataset.phReplaced) return;
    t.dataset.phReplaced = '1';
    // derive the placeholder URL from the loaded stylesheet path
    var ss = document.querySelector('link[rel="stylesheet"]');
    var base = ss ? ss.getAttribute('href').replace(/css\/[^/]+$/, '') : 'assets/';
    t.src = base + 'images/placeholder.jpg';
  }, true);
})();
