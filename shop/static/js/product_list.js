let visibility = 3;
let productBox = document.getElementById('product-box')
let loadBtn = document.getElementById('butt')


const handlData = () =>{
    $.ajax({
        type: 'GET',
        url: `json/${visibility}`,
        success: function(response){
            let data = response.data
            let maxSize = response.max
            data.map(product => {
                let slug = product.slug
                productBox.innerHTML += `<div class="card mt-3 p-3 mb-3">
                <h3>${product.name}</h3>
                <h4 style="color: red">${product.price}</h4>
                <a href="http://127.0.0.1:8000/staff/edit_product/${slug}">Подробнее</a><br>
                </div>`
            })
            if(maxSize){
                loadBtn.classList.add('non-visible')
            }
        },
        error: function(error){
            console.log(error)
        }
    })
    
}
handlData()
loadBtn.addEventListener('click',() => {
    visibility += 3
    handlData()
}) 