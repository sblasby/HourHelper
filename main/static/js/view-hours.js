function ChangeMonth() {

    const date_picker = document.querySelector('#date-picker');

    let curr_date = new Date();

    date_picker.value = curr_date.getFullYear().toString() + '-' + (curr_date.getMonth() + 1).toString().padStart(2, '0')

    dateQuery(curr_date)


    date_picker.addEventListener('change', function () {

        let date_select = new Date(date_picker.value + '-01 00:00:00');

        dateQuery(date_select);
    })

}

document.addEventListener('DOMContentLoaded', ChangeMonth)

//------------------------------------------------------------

function AddBtnClicked() {

    const add_btn = document.querySelector('#add_hours_btn')

    add_btn.addEventListener('click', function () {

        const display_modal = document.querySelector('#form_modal')
        const modal_body = document.querySelector('#modal-content')

        fetch('/add-hours/')

            .then(response => {
                if (!response.ok) {
                    alert("The add hours form could not be rendered")
                    throw new Error("Form could not be rendered")
                }

                else {
                    return response.text()
                }
            })

            .then(html => {
                modal_body.innerHTML = html;

                $(display_modal).modal('show');

                AddBtnListener()
                LessonTypeListener()

                document.dispatchEvent(new Event('modalShown'))
            })

            .catch(error => {
                alert("There was an unexpected error")
                throw new Error(error)
            })
    })
}

document.addEventListener('DOMContentLoaded', AddBtnClicked)

//----------------------------------------------------------


function AddBtnListener() {
    const save_btn = document.querySelector('#add_btn')
    const form = document.querySelector('#add_lesson_form')
    const date_pick = document.getElementById('date-picker')
    const timeout = 3000

    // Field names
    const lesson_field = document.getElementById('class_type');
    const duration_field = document.getElementById('duration')
    const date_field = document.getElementById('class_date')
    const start_field = document.getElementById('class_time')
    const student_field = document.getElementById('student');
    const school_field = document.getElementById('school')

    //Success and UnSuccess msg
    const success_msg = document.getElementById('add_success_msg')
    const fields_miss_msg = document.getElementById('fields_miss_msg')
    const unsuccess_msg = document.getElementById('add_unsuccess_msg')
    const date_msg = document.getElementById('date_small')

    const field_arr = [
        lesson_field,
        duration_field,
        date_field,
        start_field
    ];

    save_btn.addEventListener('click', function () {

        let fieldsAreEmpty = false;

        for (let i = 0; i < field_arr.length; i++) {

            const field = field_arr[i];

            if (field.value.trim() === '') {
                fieldsAreEmpty = true
                break; // Exit the loop when a field is empty
            }
        }

        if ((lesson_field.value === 'VTC Private' &&
            student_field.value.trim() === '')
            || fieldsAreEmpty) {

            fields_miss_msg.style.display = 'block';

            setTimeout(function () {
                fields_miss_msg.style.display = 'none';
            }, timeout);

        }
        else if ((lesson_field.value.split(' ')[0] === 'TenTen' &&
            school_field.value.trim() === '')) {

            fields_miss_msg.style.display = 'block';

            setTimeout(function () {
                fields_miss_msg.style.display = 'none';
            }, timeout);
        }
        else if (parseInt(date_field.value.slice(0, 4)) < 2023) {

            date_msg.style.display = 'block';

            setTimeout(function () {
                date_msg.style.display = 'none';
            }, timeout);
        }

        else {

            const form_data = new FormData(form)

            const csrftoken = getCookie('csrftoken')

            if (csrftoken === null) {
                throw new Error("CSRF could not be verified")
            }

            const request = new Request(
                '/add-hours/',
                {
                    method: 'POST',
                    body: form_data,
                    headers: { 'X-CSRFToken': csrftoken },
                    credentials: 'same-origin'
                }
            );

            fetch(request)

                .then(response => {
                    if (!response.ok) {
                        unsuccess_msg.style.display = 'block'
                        setTimeout(function () {
                            unsuccess_msg.style.display = 'none'
                        }, timeout)
                        throw new Error("Response was not ok")
                    }

                    else if (lesson_field.value === 'VTC Private') {
                        student_field.value = ''
                    }

                    field_arr.forEach(function (item) {
                        item.value = ''
                    })

                    success_msg.style.display = 'block'

                    let date_select = new Date(date_pick.value + '-01 00:00:00');

                    dateQuery(date_select);

                    setTimeout(function () {
                        success_msg.style.display = 'none'
                    }, timeout)
                })

                .catch(error => {

                    success_msg.style.display = 'block'

                    setTimeout(function () {
                        success_msg.style.display = 'none'
                    }, timeout)
                })
        }

    })
}

function LessonTypeListener() {
    const lesson_select = document.querySelector('#class_type');
    const student_field = document.querySelector('#student-field');
    const school_field = document.getElementById('school-field')

    if (lesson_select.value === 'VTC Private') {
        student_field.style.display = 'block'
    }
    else if (lesson_select.value.split(' ')[0] === 'TenTen') {
        school_field.style.display = 'block'
    }

    lesson_select.addEventListener('change', function () {

        let lesson_type = lesson_select.value

        if (lesson_type === 'VTC Private') {
            student_field.style.display = 'block'
            school_field.style.display = 'none'
        }
        else if (lesson_select.value.split(' ')[0] === 'TenTen') {
            school_field.style.display = 'block'
            student_field.style.display = 'none'
        }
        else {
            school_field.style.display = 'none'
            student_field.style.display = 'none'
        }

    })
}
//---------------------------------------------------------------
//Edit Listening
function EditListening() {
    const edit_btns = document.getElementsByName('edit_button')
    const display_modal = document.getElementById('form_modal')
    const modal_content = document.getElementById('modal-content')

    edit_btns.forEach(function (btn) {
        btn.addEventListener('click', function (event) {

            const clicked_btn = event.target
            let btn_id = clicked_btn.getAttribute('id')
            btn_id = btn_id.slice(4)

            fetch('/edit-hour-' + btn_id + '/')

                .then(response => {
                    if (!response.ok) {
                        throw new Error("Edits could not be made")
                    }
                    else {
                        return response.text()
                    }
                })

                .then(html => {

                    modal_content.innerHTML = html;
                    $(display_modal).modal('show')

                    LessonTypeListener()
                    SaveListener(btn_id)
                })

                .catch(err => {
                    alert(err)
                })

        })
    })
}

function SaveListener(dbId) {
    const date_pick = document.getElementById('date-picker')
    const save_btn = document.getElementById('save_btn')

    const success_msg = document.getElementById('edit_success_msg')
    const fields_miss_msg = document.getElementById('fields_miss_msg')
    const unsuccess_msg = document.getElementById('edit_unsuccess_msg')

    function showMessage(form_msg) {
        form_msg.style.display = 'block'

        setTimeout(function () {
            form_msg.style.display = 'block'
        }, 3000)
    }

    const lesson_field = document.getElementById('class_type');
    const duration_field = document.getElementById('duration')
    const date_field = document.getElementById('class_date')
    const start_field = document.getElementById('class_time')
    const student_field = document.getElementById('student');
    const school_field = document.getElementById('school')
    const form = document.getElementById('edit_lesson_form')

    const field_arr = [
        lesson_field,
        duration_field,
        date_field,
        start_field
    ];

    let fieldsAreEmpty = false;

    save_btn.addEventListener('click', function () {

        field_arr.forEach(function (input_field) {
            if (input_field.value.trim() === '') {
                fieldsAreEmpty = true;
            }
        })

        if ((lesson_field.value === 'VTC Private' &&
            student_field.value.trim() === '')
            || fieldsAreEmpty) {
            showMessage(fields_miss_msg)
        }
        else if ((lesson_field.value.split(' ')[0] === 'TenTen' &&
            school_field.value.trim() === '')) {
            showMessage(fields_miss_msg)
        }
        else {
            const form_data = new FormData(form)

            const csrftoken = getCookie('csrftoken')

            if (csrftoken === null) {
                throw new Error("CSRF could not be verified")
            }

            const request = new Request(
                '/edit-hour-' + dbId.toString() + '/',
                {
                    method: 'POST',
                    body: form_data,
                    headers: { 'X-CSRFToken': csrftoken },
                    mode: 'same-origin'
                }
            );

            fetch(request)

                .then(response => {
                    if (!response.ok) {
                        throw new Error("Response was not ok!")
                    }
                    else {
                        const date_select = new Date(date_pick.value + '-01 00:00:00');

                        dateQuery(date_select);

                        showMessage(success_msg)
                    }
                })

                .catch(error => {
                    showMessage(unsuccess_msg)
                })
        }

    })


}


//----------------------------------------------------------------
//Delete Btn
function DeleteListening() {
    const del_btns = document.getElementsByName('delete_button')
    // const display_modal = document.getElementById('form_modal')
    // const modal_content = document.getElementById('modal-content')

    del_btns.forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            const clicked_btn = event.target;
            let clicked_id = clicked_btn.getAttribute('id');
            clicked_id = clicked_id.slice(4);

            const csrftoken = getCookie('csrftoken')

            if (csrftoken === null) {
                throw new Error("CSRF could not be verified")
            }

            const request = new Request(
                '/delete-' + clicked_id + '/',
                {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrftoken },
                    mode: 'same-origin'
                }
            );

            fetch(request)

                .then(response => {
                    if (!response.ok) {
                        alert("Hour could not be deleted")
                        throw new Error("View response error")
                    }
                    else {
                        const date_pick = document.getElementById('date-picker')

                        const date_select = new Date(date_pick.value + '-01 00:00:00');

                        dateQuery(date_select);
                    }
                })

                .catch(err => {
                    alert(err)
                })

        })
    })

}




//-----------------------------------------------------------------
// Usefull functions

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function dateQuery(date) {

    const both_tables = document.getElementById('both-tables')

    url = '/update-tables-' + date.getFullYear().toString() + '-' + (date.getMonth() + 1).toString() + '/'


    fetch(url)

        .then(response => {
            if (!response.ok) {
                alert('There was an error trying to get the data for the selected month.')
            }
            else {
                return response.text()
            }
        })

        .then(html => {
            both_tables.innerHTML = html

            EditListening()
            DeleteListening()
        })

        .catch(error => {
            alert('An unexpected error has occured.')
            throw new Error(error)
        })

}
