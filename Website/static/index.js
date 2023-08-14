const currentPath = window.location.pathname;

function deleteNote(noteId){

    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        if (currentPath === '/my-posts') {
            window.location.href = '/my-posts';
        } else if (currentPath === '/browse') {
            window.location.href = '/browse';
        }
    });
}

if(currentPath === '/my-posts' | currentPath==='/browse'){

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

if(currentPath === '/my-posts'){
    const textarea = document.getElementById('note');
    const counter = document.getElementById('counter');
    const maxCount = 1500;

    textarea.addEventListener('input', function() {
        const remainingChars = maxCount - textarea.value.length;
        counter.innerHTML = remainingChars;
    });
}

if(currentPath === '/browse'){
    document.getElementById("browse").style.color = "white";
}
if(currentPath === '/my-posts'){
    document.getElementById("home").style.color = "white";
}
if(currentPath === '/login'){
    document.getElementById("login").style.color = "white";
}
if(currentPath === '/sign-up'){
    document.getElementById("signUp").style.color = "white";
}
if(currentPath === '/logout'){
    document.getElementById("logout").style.color = "white";
}