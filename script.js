function classifyComment() {
    const comment = document.getElementById('comment').value;
    fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: comment }),
            })
            .then(response => response.json())
            .then(data => {
                if(data.emotion == 'joy') {
                    document.getElementById("joy").style.display = "block";
                    document.getElementById("anger").style.display = "none";
                    document.getElementById("fear").style.display = "none";
                } else if (data.emotion == 'anger') {
                    document.getElementById("anger").style.display = "block";
                    document.getElementById("joy").style.display = "none";
                    document.getElementById("fear").style.display = "none";
                } else if (data.emotion == 'fear') {
                    document.getElementById("fear").style.display = "block";
                    document.getElementById("joy").style.display = "none";
                    document.getElementById("anger").style.display = "none";
                } 
            })
            .catch(error => {
                console.error('Error:', error);
            });
           
}

function closePopup() {
    document.getElementById("joy").style.display = "none";
    document.getElementById("anger").style.display = "none";
    document.getElementById("fear").style.display = "none";
}
