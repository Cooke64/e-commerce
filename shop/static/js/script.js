let alertBox, imgBox, form, name, description, images, crsf, url
//  Получаем все переменные, которые нужны при работе с формой
alertBox = document.getElementById('alert_box')
imgBox = document.getElementById('img_box')
form  = document.getElementById('my_form')
// id_name формализированное обращения к именам формы. такой id присваивается авоматически 
idName = document.getElementById('id_name')
price = document.getElementById('id_price')
images = document.getElementById('id_images')
csrf = document.getElementsByName('csrfmiddlewaretoken')

// При загрузке изображения создаем ссылку на изображение и добавляем изображение на панель отображения картинки.
images.addEventListener('change', function(){
    let img_data = images.files[0]
    let url = URL.createObjectURL(img_data)
    imgBox.innerHTML = `<img src="${url}" width="100%">`
}) 
// при нажатии добавить формируем объект и добавляем туда неободимые значения из нашей формы, из переменных, которые получили выше
form.addEventListener('submit', event=>{
    event.preventDefault()

    let formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('name', idName.value)
    formData.append('price', price.value)
    formData.append('images', images.files[0])
    // Формируем ajax запрос, передаем полученные ранее formData
    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: formData,
        success: function(response){
            handleAlerts('success', `Сохранено ${response.name}`)
            console.log(response.name)
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
        alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">${text}</div>`
    }