// for roadmap
function toggleLanguages(id) {
  console.log("Toggling:", id); // Debug
  const element = document.getElementById(id);
  if (element) {
    console.log("Element found"); // Debug
    element.classList.toggle('active');
  } else {
    console.error("Element not found:", id);
  }
}
// Mobile menu toggle
document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.querySelector('.menu').classList.toggle('active');
});
