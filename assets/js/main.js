/* =============================================
   WebGrobogan - Main JavaScript
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {
  initNavbar();
  initBackToTop();
  initContactForm();
  initCounterAnimation();
  initScrollReveal();
});

/* ---------- Navbar ---------- */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (!navbar) return;

  // Scroll behavior
  window.addEventListener('scroll', function () {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, { passive: true });

  // Mobile toggle
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('open');
      navToggle.innerHTML = isOpen
        ? '<i class="fas fa-times"></i>'
        : '<i class="fas fa-bars"></i>';
    });

    // Close menu when a link is clicked
    navMenu.querySelectorAll('.navbar__link').forEach(function (link) {
      link.addEventListener('click', function () {
        navMenu.classList.remove('open');
        navToggle.innerHTML = '<i class="fas fa-bars"></i>';
      });
    });
  }

  // Set active link based on current page
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar__link').forEach(function (link) {
    link.classList.remove('active');
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}

/* ---------- Back to Top ---------- */
function initBackToTop() {
  const btn = document.getElementById('backToTop');
  if (!btn) return;

  window.addEventListener('scroll', function () {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ---------- Contact Form ---------- */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Basic validation
    const name = form.querySelector('[name="name"]');
    const email = form.querySelector('[name="email"]');
    const message = form.querySelector('[name="message"]');
    let valid = true;

    [name, email, message].forEach(function (field) {
      if (field && !field.value.trim()) {
        field.style.borderColor = '#c62828';
        valid = false;
      } else if (field) {
        field.style.borderColor = '';
      }
    });

    if (!valid) return;

    // Simulate form submission
    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Mengirim...';
    }

    setTimeout(function () {
      const successMsg = document.getElementById('formSuccess');
      if (successMsg) {
        form.style.display = 'none';
        successMsg.style.display = 'block';
      }
    }, 1200);
  });

  // Clear error state on input
  form.querySelectorAll('input, textarea, select').forEach(function (field) {
    field.addEventListener('input', function () {
      field.style.borderColor = '';
    });
  });
}

/* ---------- Counter Animation ---------- */
function initCounterAnimation() {
  const statCards = document.querySelectorAll('.stat-card h3');
  if (statCards.length === 0) return;

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('counted');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  statCards.forEach(function (el) {
    observer.observe(el);
  });
}

/* ---------- Scroll Reveal (lightweight) ---------- */
function initScrollReveal() {
  const elements = document.querySelectorAll(
    '.card, .kuliner-card, .budaya-item, .berita-card, .wisata-card, ' +
    '.kuliner-detail-card, .budaya-detail-card, .stat-card, .layanan-card'
  );

  if (elements.length === 0) return;

  // Add initial styles
  elements.forEach(function (el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  });

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  elements.forEach(function (el) {
    observer.observe(el);
  });
}
