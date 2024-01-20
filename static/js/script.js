document.getElementById('excel-file-upload').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload-excel', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => displayPlayers(data))
    .catch(error => console.error('Error:', error));
}

function displayPlayers(players) {
    console.log(players); // For debugging
    const playerList = document.getElementById('player-list');
    playerList.innerHTML = ''; // Clear existing list

    players.forEach((player, index) => {
        const playerItem = document.createElement('div');
        playerItem.setAttribute('draggable', true);
        playerItem.setAttribute('id', 'player-' + index);
        playerItem.innerHTML = `${player.Name} - ${player.Number}`;
        playerItem.addEventListener('dragstart', handleDragStart, false);
        playerList.appendChild(playerItem);
    });
}

function handleDragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.id);
}

const playerList = document.getElementById('player-list');
const selectedPlayers = document.getElementById('selected-players');

[playerList, selectedPlayers].forEach(list => {
    list.addEventListener('dragover', handleDragOver, false);
    list.addEventListener('drop', handleDrop, false);
});

function handleDragOver(e) {
    e.preventDefault(); // Necessary for allowing a drop
}

function updateSelectedCount() {
    const count = selectedPlayers.childElementCount;
    document.getElementById('selected-count').textContent = `Selected Players: ${count}`;
}

function handleDrop(e) {
    e.preventDefault();
    const data = e.dataTransfer.getData('text/plain');
    const player = document.getElementById(data);

    // Determine the target list
    let targetList = e.target;
    while (targetList && !targetList.classList.contains('player-list') && !targetList.classList.contains('selected-players')) {
        targetList = targetList.parentNode;
    }

    // If dropping into the selected-players list
    if (targetList && targetList.classList.contains('selected-players')) {
        // Check if the selected list already has 18 players
        if (targetList.childElementCount < 18) {
            targetList.appendChild(player);
            updateSelectedCount(); // Update the count
        }
    }
    // If dropping back into the player-list
    else if (targetList && targetList.classList.contains('player-list')) {
        targetList.appendChild(player);
        updateSelectedCount(); // Update the count when removing players
    }
}

function createConvo() {
    const selectedPlayersElements = document.getElementById('selected-players').children;
    const playerData = Array.from(selectedPlayersElements).map(player => {
        return { name: player.textContent.split(' - ')[0], number: player.textContent.split(' - ')[1] };
    });

    fetch('/create-convo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ players: playerData })
    })
    .then(response => response.blob())
    .then(blob => {
        // Create a link and download the image
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'convo_image.png'; // Name the download
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('build-convo').addEventListener('click', function() {
       // Example: get coach and date from input fields or other elements
    const coach = document.getElementById('coach-input').value;
    const teams = document.getElementById('teams-input').value;
    const date = document.getElementById('date-input').value;
    const selectedPlayersElements = document.getElementById('selected-players').children;
    const playerData = Array.from(selectedPlayersElements).map(playerElement => {
        const [name, number] = playerElement.textContent.split(' - ');
        return { name, number };
    });

    fetch('/build-convo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selected_players: playerData,coach: coach, date: date,teams: teams})
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'convo_image.png';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
});



document.getElementById('upload-template').addEventListener('click', function() {
    const fileInput = document.getElementById('template-file-upload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file!');
        return;
    }

    const formData = new FormData();
    formData.append('template', file);

    fetch('/upload-template', {
        method: 'POST',
        body: formData  // FormData object, no need to set Content-Type header
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Template uploaded successfully!');
        } else {
            alert('Upload failed!');
        }
    })
    .catch(error => console.error('Error:', error));
});
