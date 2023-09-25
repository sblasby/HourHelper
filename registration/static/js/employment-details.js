document.addEventListener('DOMContentLoaded', Listeners)

function Listeners(){
    const Ten_check =  document.getElementById('TenTen-check')
    const VTC_check = document.getElementById('VTC-check')
    
    Ten_check.addEventListener('change',function(){
        BoxClicked('TenTen', Ten_check)
    })

    VTC_check.addEventListener('change', function(){
        BoxClicked('VTC', VTC_check)
    })

}

function BoxClicked(name, field){
    const extra_details = document.getElementById(name + '-details')

    if (field.checked){
        extra_details.style.display = 'block'
    }
    else{
        extra_details.style.display = 'none'
    }

}