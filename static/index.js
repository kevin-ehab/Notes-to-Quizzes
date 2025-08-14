const timerButton = document.getElementById('timerButton');
const timerInput = document.getElementById('timerInput');

let timerOn = false;

timerButton.addEventListener('click', () => {
    timerOn = !timerOn;

    if (timerOn) {
        timerButton.textContent = "On";
        timerButton.style.backgroundColor = "green";
        timerInput.style.display = "inline-block";
    } else {
        timerButton.textContent = "Off";
        timerButton.style.backgroundColor = "red";
        timerInput.style.display = "none";
    }
});

const btn = document.getElementById('generate')

btn.addEventListener('click', ()=>{
    let notes = document.getElementById('notes').value
    let number = document.getElementById('number').value
    let timer = timerOn ? timerInput.value * 60 : null;
    fetch('/notes', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({notes, number, timer})
    })
    .then(res => res.json())
    .then(data => {
        if (data.message){
            alert(data.message)
        }else{
            window.location = '/quiz'
        }
        
    })
    
})