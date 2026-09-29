const search = document.querySelector('#spell-search');
if (search) {
  const cards = [...document.querySelectorAll('.spell-card')];
  const filter = () => {
    const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => { card.hidden = !words.every(word => card.dataset.search.includes(word)); if (!card.hidden) count++; });
    document.querySelector('#spell-count').textContent = `${count} of ${cards.length} spells`;
    document.querySelector('#no-spells').hidden = count !== 0;
  };
  search.addEventListener('input', filter);
  document.querySelector('#clear-search').addEventListener('click', () => { search.value = ''; filter(); search.focus(); });
}
