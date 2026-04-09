/**
 * Website Pemerintah Kabupaten Grobogan
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Current Date in Topbar ──────────────────────────────────
  const dateEl = document.getElementById('currentDate');
  if (dateEl) {
    const opts = { weekday:'long', year:'numeric', month:'long', day:'numeric' };
    dateEl.textContent = new Date().toLocaleDateString('id-ID', opts);
  }

  // ── Navbar scroll effect ────────────────────────────────────
  const navbar = document.getElementById('mainNavbar');
  const onScroll = () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  // ── Active nav link highlight on scroll ────────────────────
  const sections = document.querySelectorAll('section[id], div[id]');
  const navLinks = document.querySelectorAll('#navbarMain .nav-link');

  const highlightNav = () => {
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 120) {
        current = sec.getAttribute('id');
      }
    });
    navLinks.forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (href && href === `#${current}`) link.classList.add('active');
    });
  };
  window.addEventListener('scroll', highlightNav, { passive: true });

  // ── Smooth scroll for anchor links ─────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const offset = navbar ? navbar.offsetHeight + 8 : 80;
      window.scrollTo({
        top: target.offsetTop - offset,
        behavior: 'smooth'
      });
      // Close mobile nav if open
      const collapseEl = document.getElementById('navbarMain');
      if (collapseEl && collapseEl.classList.contains('show')) {
        bootstrap.Collapse.getInstance(collapseEl)?.hide();
      }
    });
  });

  // ── Back to Top button ──────────────────────────────────────
  const backTopBtn = document.getElementById('backToTop');
  if (backTopBtn) {
    window.addEventListener('scroll', () => {
      backTopBtn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    backTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Complaint form submit ───────────────────────────────────
  const form = document.getElementById('complaintForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
      }
      // Show success toast
      showToast(
        'Pengaduan Terkirim',
        'Pengaduan Anda telah berhasil dikirim. Kami akan menindaklanjuti dalam 3×24 jam.',
        'success'
      );
      form.reset();
      form.classList.remove('was-validated');
    });
  }

  // ── Simple Toast Notification ───────────────────────────────
  function showToast(title, message, type = 'success') {
    const colors = {
      success: { bg: '#16a34a', icon: 'bi-check-circle-fill' },
      error:   { bg: '#dc2626', icon: 'bi-x-circle-fill' },
      info:    { bg: '#2563aa', icon: 'bi-info-circle-fill' },
    };
    const c = colors[type] || colors.info;

    const container = getOrCreateToastContainer();
    const id = `toast-${Date.now()}`;
    const html = `
      <div id="${id}" class="toast align-items-center border-0 text-white show"
           role="alert" style="background:${c.bg}; min-width:280px;">
        <div class="d-flex">
          <div class="toast-body d-flex align-items-start gap-2">
            <i class="bi ${c.icon} fs-5 flex-shrink-0 mt-1"></i>
            <div>
              <div class="fw-bold">${title}</div>
              <div class="small opacity-90">${message}</div>
            </div>
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto"
                  data-bs-dismiss="toast"></button>
        </div>
      </div>`;
    container.insertAdjacentHTML('beforeend', html);
    const toastEl = document.getElementById(id);
    const bsToast = new bootstrap.Toast(toastEl, { delay: 5000 });
    bsToast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
  }

  function getOrCreateToastContainer() {
    let c = document.getElementById('toastContainer');
    if (!c) {
      c = document.createElement('div');
      c.id = 'toastContainer';
      c.style.cssText = 'position:fixed;top:1.25rem;right:1.25rem;z-index:1100;display:flex;flex-direction:column;gap:.5rem;';
      document.body.appendChild(c);
    }
    return c;
  }

  // ── Animate stat numbers on first view ─────────────────────
  const statNums = document.querySelectorAll('.stat-number');
  const animated = new Set();

  const animateNum = (el) => {
    const raw   = el.textContent.trim();
    const match = raw.match(/[\d,]+/);
    if (!match) return;
    const target = parseInt(match[0].replace(/,/g, ''), 10);
    const suffix = raw.replace(match[0], '');
    let current  = 0;
    const step   = Math.ceil(target / 60);
    const timer  = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current.toLocaleString('id-ID') + suffix;
      if (current >= target) clearInterval(timer);
    }, 20);
  };

  const statObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated.has(entry.target)) {
        animated.add(entry.target);
        animateNum(entry.target);
      }
    });
  }, { threshold: 0.3 });

  statNums.forEach(el => statObserver.observe(el));

  // ── Fade-in on scroll for cards ────────────────────────────
  const fadeEls = document.querySelectorAll('.service-card, .news-card-main, .news-card-sm, .announcement-card, .visi-misi-card, .tourism-card');
  fadeEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity .5s ease, transform .5s ease';
  });

  const fadeObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, 80);
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  fadeEls.forEach(el => fadeObserver.observe(el));

});
