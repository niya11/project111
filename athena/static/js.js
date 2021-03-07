var data;
function stockSummary(x) {
        var url = "/covid_data?q=" + x;
        var form_request = new XMLHttpRequest();
        form_request.open("GET", url, true);

         form_request.onreadystatechange = function () {
            if (form_request.readyState === XMLHttpRequest.DONE ) {

                if (this.status >= 200 && this.status < 400) {
                    jsondoc = JSON.parse(form_request.responseText);
                    console.log(jsondoc);

                }

            }
         }
         populate_covid_data(jsondoc);
         data=jsondoc
        form_request.send()
        populate_covid_data();
        window.location.href = "/static/nicki.html";
        //populate_covid_data(jsondoc);
    }
    
function populate_covid_data(){
    console.log(data)
}