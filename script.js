function addOrder() {
    const type = document.getElementById('orderType').value;
    const budget = document.getElementById('budget').value;
    const whatsapp = document.getElementById('whatsapp').value;
    const description = document.getElementById('description').value;
  
    if (!budget || !whatsapp || !description) {
      alert("Барлық өрістерді толтырыңыз!");
      return;
    }
  
    const sectionId = 'section-' + type;
    const section = document.getElementById(sectionId);
  
    const card = document.createElement('div');
    card.className = 'order-card';
    card.innerHTML = `
      <h4>${type}</h4>
      <p>${description}</p>
      <p><strong>Бюджет:</strong> ₸${budget}</p>
      <a class="whatsapp-btn" href="https://wa.me/${whatsapp.replace(/\D/g, '')}" target="_blank">
        Whatsapp арқылы жазу
      </a>
    `;
  
    section.appendChild(card);
  
    // Форманы тазалау
    document.getElementById('budget').value = '';
    document.getElementById('whatsapp').value = '';
    document.getElementById('description').value = '';
  }
  