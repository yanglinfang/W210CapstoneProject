
function updateSimTextInput(val) {
    $('#simText').text(val)
};

function updateTopTextInput(val) {
    $('#topText').text(val)
};


function toggleShow(id){
    var full = id.replace('_more', '_full');
    var less = id.replace('_more', '_less');

    if($('#'+id).text()=='... ...more'){
        $('#'+id).text('less');
        $('#'+full).removeAttr('hidden')
        $('#'+full).show();
        $('#'+less).hide()
    }
    else{
        $('#'+id).text('... ...more');
        $('#'+full).hide();
        $('#'+less).show()
    }
}
    
function showMore(fullText, lengthLim, id){
    var firstHalf = fullText.substring(0, lengthLim)
    var d = document.createElement("td");
    if(fullText.length <=lengthLim){
        d.innerHTML='<span class="complete" id="'+id+'_full'+'">' + fullText + '</span>' 
    }
    else{
        d.innerHTML='<span class="teaser" id="'+id+'_less'+'">'+firstHalf+'</span>' + '<span class="complete" hidden="hidden" id="'+id+'_full'+'">' + fullText + '</span><span class="more" style="color: blue;" onclick="toggleShow(this.id)" id="'+id+'_more'+'">... ...more</span>' 
    }
    return d;
}

function changeClusters(cluster1, cluster2) {
    $('iframe')[0].src =
        "http://" + document.location.host + "/patent/wordcloud/" + cluster1 + "+" + cluster2 + "+400"
    $('iframe')[1].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+pub_year"
    $('iframe')[2].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+appl_year"
    $('iframe')[3].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+grant_year"
    $('iframe')[4].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+years_to_publish"
    $('iframe')[5].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+years_to_grant"
    $('iframe')[6].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+patent_doc_kind"
    $('iframe')[7].src =
        "http://" + document.location.host + "/patent/patentstats/" + cluster1 + "+" + cluster2 + "+number_of_claims"
}

function searchPatents() {
    //console.log('search clicked');
    $('#loader').attr("class","loader")
    $("#searchresultTable > tbody").empty();

    $('#clusterInfo').text('')

    hosturl = 'http://ec2-54-89-199-144.compute-1.amazonaws.com:8080/patentsearch'
    var srchtext = $('#searchtext').val().trim();
    var topX = $('#top').val()
    var similarity = $('#sim').val() / 100;

    if(srchtext == ""){
        return; 
    }

    srchurl = hosturl + '?query_string=' + srchtext + '&top=' + topX + '&cosine_sim_threshold=' + similarity;

    $.ajax({
        type: "GET",
        url: srchurl,
        dataType: "json",
        contentType: "application/json",
        crossDomain: true,
        success: function (data) {
            console.log(data);
            $('#loader').attr("class","")
           
            searchresult_data = data.searchresult;
            cluster1 = data.firstcluster;
            cluster2 = data.secondcluster;
            changeClusters(cluster1, cluster2);
            $('#clusterInfo').text('First level cluster ' + str(int(cluster1)+1) + '. Second level cluster ' + str(int(cluster2)+1)) + '.';

            var output = document.querySelector('#searchresultTable tbody');

            for (var i = 0; i < searchresult_data.length; i++) {
                //console.log(searchresult_data[i].appl_doc_number);
                var row = document.createElement('tr');

                var td = document.createElement('td');
                td.appendChild(document.createTextNode(searchresult_data[i].appl_doc_number));
                row.appendChild(td);

                var td = document.createElement('td');
                var p_num = searchresult_data[i].patent_number;
                if(p_num == null){
                    p_num = 'N/A'
                }
                td.appendChild(document.createTextNode(p_num));
                row.appendChild(td);

                var td = document.createElement('td');
                td.appendChild(document.createTextNode((searchresult_data[i].cosine_similarity * 100).toFixed(2)));
                row.appendChild(td);

                var td = document.createElement('td');
                td.appendChild(document.createTextNode(searchresult_data[i].invention_title));
                row.appendChild(td);

                //var td = document.createElement('td');
                //td.appendChild(document.createTextNode(searchresult_data[i].abstract));
                //row.appendChild(td);					

                var lengthLimit = 200
                var abstract = searchresult_data[i].abstract
                row.appendChild(showMore(abstract, lengthLimit, searchresult_data[i].appl_doc_number + '_abs'));

                var claim_text = searchresult_data[i].claim_text
                row.appendChild(showMore(claim_text, lengthLimit, searchresult_data[i].appl_doc_number + '_claim'));

                output.appendChild(row);
            }
        }
    });
};

