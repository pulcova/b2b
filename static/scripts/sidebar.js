
   // Get references to the button, sidebar, and other elements
   const drawerButton = document.querySelector('[data-drawer-target="cta-button-sidebar"]');
   const drawerToggle = document.querySelector('[data-drawer-toggle="cta-button-sidebar"]');
   const sidebar = document.getElementById('cta-button-sidebar');
   const dropdownToggles = document.querySelectorAll('[data-collapse-toggle]');
 
   // Click Event for Opening/Closing the Sidebar
   drawerButton.addEventListener('click', () => {
     sidebar.classList.toggle('-translate-x-full');
   });
 
   drawerToggle.addEventListener('click', () => {
     sidebar.classList.toggle('-translate-x-full');
   });
 
   // Handling Dropdown Menus
   dropdownToggles.forEach(button => {
     button.addEventListener('click', () => {
       const dropdownMenu = button.nextElementSibling;
       if (dropdownMenu && dropdownMenu.classList.contains('hidden')) {
         dropdownMenu.classList.remove('hidden');
 
         // Save in localStorage
         const menuId = button.getAttribute('data-collapse-toggle');
         localStorage.setItem(menuId, true); 
 
       } else {
         dropdownMenu.classList.add('hidden');
 
         // Save in localStorage
         const menuId = button.getAttribute('data-collapse-toggle');
         localStorage.setItem(menuId, false); 
       }
     });
   });
 
   // On page load, restore states
   window.addEventListener('load', () => {
     dropdownToggles.forEach(button => {
       const menuId = button.getAttribute('data-collapse-toggle');
       const shouldBeOpen = localStorage.getItem(menuId) === 'true';
       if (shouldBeOpen) {
         button.nextElementSibling.classList.remove('hidden');
       }
     });
   });

 