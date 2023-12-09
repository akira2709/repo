const price = Number(document.getElementById('price').textContent)
const down = document.getElementById('down')
const file = document.getElementById('file').textContent
const user_balance = Number(document.getElementById('user_balance').textContent)
down.onclick = () =>{
  console.log(user_balance, price)
  if (user_balance >= price){
    var link = document.createElement('a')
    link.href = file
    link.download = file

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } else {
    alert('У вас недостаточно средств!')
  }
}