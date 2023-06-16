function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href="/";
    });
}


const cards = document.querySelectorAll('.card');

cards.forEach(card => {
    let isMouseOverCard = false;

    card.addEventListener('mouseover', () => {
        isMouseOverCard = true;
        const deleteButton = card.querySelector('.delete-button');
        deleteButton.style.opacity = 0.75;
        deleteButton.style.transition = 'opacity 0.2s ease-in-out';
    });

    card.addEventListener('mouseout', () => {
        isMouseOverCard = false;
        const deleteButton = card.querySelector('.delete-button');
        deleteButton.style.opacity = 0;
        deleteButton.style.transition = 'opacity 0.2s ease-in-out';
    });

    if (!isMouseOverCard) {
        const deleteButton = card.querySelector('.delete-button');
        deleteButton.style.opacity = 0;
        deleteButton.style.transition = 'opacity 0.2s ease-in-out';
    }
});