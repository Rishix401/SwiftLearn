document.addEventListener('DOMContentLoaded', function() {
    const links = [
      { id: 'courses-link', container: 'courses-container' },
      { id: 'dates-link', container: 'dates-container' },
      { id: 'discussions-link', container: 'discussions-container' },
      { id: 'faqs-link', container: 'faqs-container' },
    ];

    document.querySelector('#courses-link').classList.add('border-bottom');

  
    links.forEach(link => {
      const linkEl = document.querySelector(`#${link.id}`);
      const containerEl = document.querySelector(`#${link.container}`);
  
      linkEl.addEventListener('click', () => {
        links.forEach(otherLink => {
          const otherLinkEl = document.querySelector(`#${otherLink.id}`);
          const otherContainerEl = document.querySelector(`#${otherLink.container}`);
  
          if (link.id === otherLink.id) {
            containerEl.style.display = 'block';
            otherLinkEl.classList.add('border-bottom');
          } else {
            otherContainerEl.style.display = 'none';
            otherLinkEl.classList.remove('border-bottom');
          }
        });
      });
    });

    document.querySelector('#lectures-link').lastElementChild.style.border = 'none';
  });
  