function sendEmailXhttp() {
    var event_id = document.getElementById('events_list').value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/sendemail/" + event_id, true);
    xhttp.send();
    toastr.success("Email has been sent");
}