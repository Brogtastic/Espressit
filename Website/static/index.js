const currentPath = window.location.pathname;

function deleteNote(noteId){

    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        if (currentPath === '/') {
            window.location.href = '/';
        } else if (currentPath === '/browse') {
            window.location.href = '/browse';
        }
    });
}

if(currentPath === '/' | currentPath==='/browse'){
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        let isMouseOverCard = false;

        card.addEventListener('mouseover', () => {
            isMouseOverCard = true;
            const deleteButton = card.querySelector('.delete-button');
            if (deleteButton) {
                deleteButton.style.opacity = 0.3;
                deleteButton.style.transition = 'opacity 0.2s ease-in-out';
            }
        });

        card.addEventListener('mouseout', () => {
            isMouseOverCard = false;
            const deleteButton = card.querySelector('.delete-button');
            if (deleteButton) {
                deleteButton.style.opacity = 0;
                deleteButton.style.transition = 'opacity 0.2s ease-in-out';
            }
        });


        if (!isMouseOverCard) {
            isMouseOverCard = false;
            const deleteButton = card.querySelector('.delete-button');
            if (deleteButton) {
                deleteButton.style.opacity = 0;
            }
        }
    });
}

if(currentPath === '/'){
    const textarea = document.getElementById('note');
    const counter = document.getElementById('counter');
    const maxCount = 1500;

    textarea.addEventListener('input', function() {
        const remainingChars = maxCount - textarea.value.length;
        counter.innerHTML = remainingChars;
    });
}

