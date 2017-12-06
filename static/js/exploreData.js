/* When the user clicks on the button, 
                               toggle between hiding and showing the dropdown content */
function changeCluster(v) {
    $('iframe')[0].src =
    "http://" + document.location.host + "/patent/wordcloud/x+" + v + "+400"
    $('iframe')[1].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+pub_year"
    $('iframe')[2].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+appl_year"
    $('iframe')[3].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+grant_year"
    $('iframe')[4].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+years_to_publish"
    $('iframe')[5].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+years_to_grant"
    $('iframe')[6].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+patent_doc_kind"
    $('iframe')[7].src =
    "http://" + document.location.host + "/patent/patentstats/" + v + "+x+number_of_claims"
}
