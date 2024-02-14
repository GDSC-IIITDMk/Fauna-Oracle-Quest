const textn =document.querySelector('.textn');
const texty =document.querySelector('.texty');
const question =document.querySelector('.question');
const map =document.querySelector('.map');

texty.addEventListener('click',() => {
       question.innerHTML ="Does it have legs"
       texty.addEventListener('click',() => {
        question.innerHTML ="Is it domestic"
    });
});