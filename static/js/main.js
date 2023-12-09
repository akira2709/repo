const files = document.getElementById('files').textContent.split(' ')
const balance = Number(document.getElementById('balance').textContent)
const total = Number(document.getElementById('total').textContent)
function downloadFiles() {
  if (balance >= total && total > 0){
    var fileUrls = files;
    fileUrls.forEach(function (url) {
      var link = document.createElement('a');
      link.href = url;
      link.download = url.substr(url.lastIndexOf('/') + 1);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  } else if (total > 0){
    alert('У вас недостаточно средств!')
  }
}


