const form = document.getElementById("review-form");
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const divComment = document.getElementById('reviews')
const messageValue = document.getElementById('id_text')


form.addEventListener("submit", (event)=>{
    event.preventDefault();
  let message = messageValue.value;
  let formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrf[0].value)
  formData.append('message', message)
  $.ajax({
    type: 'POST',
    url: '',
    enctype: 'multipart/form-data',
    data: formData,
    success: function(response){
        handleAlerts('success', message)
        console.log('done')
    },
    error: function(error){
        handleAlerts('danger', 'Не сохранено. Какая-то ошибка')
    },
    cache: false,
    contentType: false,
    processData: false,
    })
  
})

let handleAlerts = (type, text) =>{
    divComment.innerHTML = `<div class="alert alert-${type}" role="alert">${text}</div>`
}