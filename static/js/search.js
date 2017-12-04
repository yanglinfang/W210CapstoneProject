function searchPatents() {
    console.log('search clicked');
    $("#searchresultTable > tbody").empty();

    hosturl = 'http://ec2-54-89-199-144.compute-1.amazonaws.com:8080/patentsearch'
    var srchtext = $('#searchtext').val();
    var topX = $('#top').text().trim()
    var similarity = $('#sim').text().trim()
    srchurl = hosturl + '?query_string=' + srchtext + '&top='+topX+'&cosine_sim_threshold='+similarity;

    $.ajax({
        type: "GET",
        url: srchurl,
        dataType: "json",
        contentType: "application/json",
        crossDomain: true,
        success: function (data) {
            console.log(data);
            chart_data = data.charts_data.charts_data1;
            searchresult_data = data.searchresult;

            var output = document.querySelector('#searchresultTable tbody');

            for (var i = 0; i < searchresult_data.length; i++) {
                //console.log(searchresult_data[i].appl_doc_number);
                var row = document.createElement('tr');

                var td = document.createElement('td');
                td.appendChild(document.createTextNode(searchresult_data[i].appl_doc_number));
                row.appendChild(td);

                var td = document.createElement('td');
                td.appendChild(document.createTextNode(searchresult_data[i].invention_title));
                row.appendChild(td);

                //var td = document.createElement('td');
                //td.appendChild(document.createTextNode(searchresult_data[i].abstract));
                //row.appendChild(td);					

                var abstract = searchresult_data[i].abstract

                if (abstract.length > 150) {
                    abstract_small = abstract.substring(0, 150) + '....'

                    var abbrnode = document.createElement("abbr");
                    abbrnode.setAttribute("title", abstract);
                    var abbrtextnode = document.createTextNode(abstract_small);
                    abbrnode.appendChild(abbrtextnode);
                    var td = document.createElement('td');
                    td.appendChild(abbrnode);
                    row.appendChild(td);
                }
                else {
                    var td = document.createElement('td');
                    td.appendChild(document.createTextNode(abstract));
                    row.appendChild(td);
                }


                var claim_text = searchresult_data[i].claim_text

                if (claim_text.length > 150) {
                    claim_text_small = claim_text.substring(0, 150) + '....'

                    var abbrnode = document.createElement("abbr");
                    abbrnode.setAttribute("title", claim_text);
                    var abbrtextnode = document.createTextNode(claim_text_small);
                    abbrnode.appendChild(abbrtextnode);
                    var td = document.createElement('td');
                    td.appendChild(abbrnode);
                    row.appendChild(td);
                }
                else {
                    var td = document.createElement('td');
                    td.appendChild(document.createTextNode(claim_text));
                    row.appendChild(td);
                }

                output.appendChild(row);
            }
        }
    });
};