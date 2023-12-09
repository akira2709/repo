const all_filled = Number(document.getElementById('all_filled').textContent)
const ps = Number(document.getElementById('ps').textContent)
const used_name = Number(document.getElementById('used_name').textContent)
if (used_name === 1){
    alert('Данное имя уже использовано!')
}
else if (all_filled === 0){
    alert('Заполните все поля!')
}
else if (ps === 0){
    alert('Пароли не совпадают!')
}
