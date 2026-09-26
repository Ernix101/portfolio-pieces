const cards = document.querySelectorAll('.appointment-card');
const drawer = document.querySelector('.patient-drawer');
const drawerClose = document.querySelector('.drawer-close');
const searchInput = document.querySelector('.search-input');
const dropdown = document.querySelector('.search-dropdown');


// patient page js
const patientDetailsDrawer = document.querySelector('.patient-details-drawer');
const listCards = document.querySelectorAll('.list-card');
const patientDrawerClose = document.querySelector('.patient-details-drawer-close');


// ----------------------------------The data used in drawer pulled by js and returned as text content-----------------------
cards.forEach(card => {
    card.addEventListener('click', () => {
        drawer.querySelector('.patient-name').textContent = card.dataset.patientName;
        drawer.querySelector('.patient-age').textContent = card.dataset.patientAge;
        drawer.querySelector('.patient-condition').textContent = card.dataset.patientCondition;
        drawer.querySelector('.provider-name').textContent = card.dataset.providerName;
        drawer.querySelector('.appt-time').textContent = card.dataset.time;
        drawer.querySelector('.appt-duration').textContent = card.dataset.duration;                         // <-- this area shows how js pulls data to the page and renders it as textcontent
        drawer.querySelector('.appt-status').textContent = card.dataset.status;
        drawer.querySelector('.status-label').className = 'status-label status-' + card.dataset.statusRaw;
        drawer.querySelector('.appt-type').textContent = card.dataset.type;

        const checkinForm = drawer.querySelector('.checkin-form');
        checkinForm.action = `/appointments/${card.dataset.appointmentId}/status/checked_in/`;
        const cancelForm = drawer.querySelector('.cancel-form');
        cancelForm.action = `/appointments/${card.dataset.appointmentId}/status/canceled/`;

        drawer.classList.toggle('hidden');
    });
});



listCards.forEach(listCard => {
    listCard.addEventListener('click', () => {
        patientDetailsDrawer.querySelector('.patient-name').textContent = listCard.dataset.patientName;
        patientDetailsDrawer.querySelector('.patient-age').textContent = listCard.dataset.patientAge;
        patientDetailsDrawer.querySelector('.patient-condition').textContent = listCard.dataset.patientCondition;
        patientDetailsDrawer.querySelector('.provider-name').textContent = listCard.dataset.providerName;
        patientDetailsDrawer.querySelector('.appt-time').textContent = listCard.dataset.time;
        patientDetailsDrawer.querySelector('.appt-duration').textContent = listCard.dataset.duration;
        patientDetailsDrawer.querySelector('.appt-status').textContent = listCard.dataset.status;
        patientDetailsDrawer.querySelector('.status-label').className = 'status-label status-' + listCard.dataset.statusRaw;
        patientDetailsDrawer.querySelector('.appt-type').textContent = listCard.dataset.type;

        // const checkinForm = patientDetailsDrawer.querySelector('.checkin-form');
        // checkinForm.action = `/appointments/${listCard.dataset.appointmentId}/status/checked_in/`;
        // const cancelForm = patientDetailsDrawer.querySelector('.cancel-form');
        // cancelForm.action = `/appointments/${listCard.dataset.appointmentId}/status/canceled/`;

        patientDetailsDrawer.classList.toggle('hidden');
    });
});


//* The close button in the calendar and patient drawers respectively (closes the drawer when clicked)
drawerClose.addEventListener('click', () => {
    drawer.classList.add('hidden');
});

if (patientDrawerClose) {
    patientDrawerClose.addEventListener('click', () => {
        patientDetailsDrawer.classList.add('hidden');
    });
}

// --------------------------------------Searching function for finding appointment (fetch in the dropdown)------------------------------------------
// * Testing the fetch function works in the console
//// searchInput.addEventListener('input', () => {
// //    const query = searchInput.value;

////     if (query.length < 2) return;

////     fetch(`/search/?q=${query}`)
////         .then(response => response.json())
// //        .then(data => {
////             console.log(data.results);
//  //       });
//// });

//*   The search bar's actual logic
searchInput.addEventListener('input', () => {
    const query = searchInput.value;

    if (query.length < 2) {
        dropdown.classList.add('hidden');
        return;
    }

    fetch(`/search/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            dropdown.innerHTML = '';

            data.results.forEach(result => {
                const item = document.createElement('div');
                item.classList.add('search-result-item');
                item.textContent = `${result.patient_name} - ${result.provider_name}`;

                item.dataset.patientName = result.patient_name;
                item.dataset.patientAge = result.patient_age;
                item.dataset.patientCondition = result.patient_condition;
                item.dataset.providerName = result.provider_name;
                item.dataset.time = result.time;
                item.dataset.duration = result.duration;
                item.dataset.status = result.status;
                item.dataset.type = result.appointment_type;
                item.dataset.appointmentId = result.id;

                item.addEventListener('click', () => {
                    drawer.querySelector('.patient-name').textContent = item.dataset.patientName;
                    drawer.querySelector('.patient-age').textContent = item.dataset.patientAge;
                    drawer.querySelector('.patient-condition').textContent = item.dataset.patientCondition;
                    drawer.querySelector('.provider-name').textContent = item.dataset.providerName;
                    drawer.querySelector('.appt-time').textContent = item.dataset.time;
                    drawer.querySelector('.appt-duration').textContent = item.dataset.duration;
                    drawer.querySelector('.appt-status').textContent = item.dataset.status;
                    drawer.querySelector('.status-label').className = 'status-label status-' + item.dataset.status;
                    drawer.querySelector('.appt-type').textContent = item.dataset.type;
                    
                    
                    const checkInForm = drawer.querySelector('.checkin-form');
                    checkInForm.action = `/appointments/${item.dataset.appointmentId}/status/checked_in/`;
                    const cancelForm = drawer.querySelector('.cancel-form');
                    cancelForm.action = `/appointments/${item.dataset.appointmentId}/status/canceled/`;

                    drawer.classList.remove('hidden');
                    dropdown.classList.add('hidden');
                });
                dropdown.appendChild(item);
            });
            
            dropdown.classList.remove('hidden');
        });
});

// -----------------------------clicking outside the dropdown to close it-----------------------------------
document.addEventListener('click', (event) => {
    const clickedInsideDropdown = dropdown.contains(event.target);
    const clickedInsideSearchInput = searchInput.contains(event.target);
    

    if (!clickedInsideDropdown && !clickedInsideSearchInput) {
        dropdown.classList.add('hidden');
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key == 'Escape') {
        dropdown.classList.add('hidden');
        drawer.classList.add('hidden');
    }
});

document.addEventListener('click', (event) => {
    const clickedInsideDropdown = dropdown.contains(event.target);
    const clickedInsideSearchInput = searchInput.contains(event.target);
    const clickedInsideDrawer = drawer.contains(event.target);
    const clickedOnAPill = event.target.closest('.appointment-card');
    const clickedOnDropdownItem = event.target.closest('.search-result-item');

    if (!clickedInsideDropdown && !clickedInsideSearchInput) {
        dropdown.classList.add('.hidden');
    }
    
    if (!clickedInsideDrawer && !clickedOnAPill && !clickedOnDropdownItem) {
        drawer.classList.add('hidden');
    }
});