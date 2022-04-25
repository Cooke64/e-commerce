let url = document.location.href
let imgDiv = document.getElementById('img')

$.ajax(
    {
        type: 'GET',
        url: `data_json/`,
        success: (response) => {
            let data = JSON.parse(response.data)
            data.forEach(element => {
                console.log(element.fields)
                if ( element.fields.images){
                    imgDiv.innerHTML+=`
                    <a href='#' data-bs-toggle="modal" data-bs-target="#preview"><img style="width:300px; height: 30px" src="media/${ element.fields.images }"></a>`
                
                }

            });
        },
        error: (error) => {
            
        }
    }
)