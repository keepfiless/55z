// for roadmap
function toggleLanguages(id) {
  const element = document.getElementById(id);
  element.classList.toggle('active');
}
// Mobile menu toggle
document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.querySelector('.menu').classList.toggle('active');
});
