const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');

tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
        
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.add('hidden'));
        tab.classList.add('active');
        contents[index].classList.remove('hidden');
    });
});


let checkboxes = document.querySelectorAll('.menu-item-check')
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('click', (e) => {
        e.preventDefault();

        const menuItemId = parseInt(e.target.dataset.id);
        const newState = e.target.checked;
        console.log("newState", newState);

        fetch('changeMenuItemAvailability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                menuItemId: menuItemId,
                newState: newState,
            }),
        })
        .then(response => {
            if (response.ok) e.target.checked = newState;
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
});

