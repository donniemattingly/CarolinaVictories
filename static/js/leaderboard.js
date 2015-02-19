/**
 * Created by dmatt on 2/16/15.
 */
var sort = "victorycount";
var sort_ascending = true;
var desc_span = "<span class=\"glyphicon glyphicon-sort-by-attributes\" aria-hidden=\"true\"></span>";
var asc_span = "<span class=\"glyphicon glyphicon-sort-by-attributes-alt\" aria-hidden=\"true\"></span>";

function clearTable(){
    $("#leaderboard-table").find('tbody').html('');
}

function sortList(){
    var ltable = $("#leaderboard-table").find('tbody')
    $.getJSON($SCRIPT_ROOT + '/_sortmemberslist/'+sort, {}, function(data){
        clearTable();
        var body = $("#leaderboard-table").find('tbody');
        for(var i=0;i<data.length;i++){
            if(sort_ascending){
                var obj = data[i];
            }
            else{
                var obj = data[data.length-i-1]
            }
            var url = '/members/'+ $.trim(obj.name).replace(' ','_');
            ltable.append("<tr><td class=name><a href=\""+url+"\">"+obj.name+"</a>"
                +"</td><td class=instrument>"+obj.instrument
                +"</td><td class=year>"+obj.year
                +"</td><td class=victorycount>"+obj.victorycount
                +"</td></tr>");
        }
    });
}

function clearSort(){
    document.getElementById("headName").innerHTML = "Name";
    document.getElementById("headInstrument").innerHTML = "Instrument";
    document.getElementById("headYear").innerHTML = "Year";
    document.getElementById("headVictories").innerHTML = "Victories"
}
function sortByName(){
    if(sort == "name"){
        sort_ascending = !sort_ascending;
    }
    else{
        sort_ascending = true;
        sort = "name";
    }
    clearSort()
    if(sort_ascending){
       document.getElementById("headName").innerHTML = "Name "+asc_span;
    }
    else{
        document.getElementById("headName").innerHTML = "Name "+desc_span;
    }
    sortList();
}

function sortByInstrument(){
    if(sort=="instrument"){
        sort_ascending = !sort_ascending;
    }
    else{
        sort_ascending=true;
        sort="instrument"
    }
    clearSort()
    if(sort_ascending){
        document.getElementById("headInstrument").innerHTML = "Instrument "+asc_span;
    }
    else{
        document.getElementById("headInstrument").innerHTML = "Instrument "+desc_span;
    }
    sortList();
}

function sortByYear(){
    if(sort=="year"){
        sort_ascending = !sort_ascending;
    }
    else{
        sort_ascending=false;
        sort="year"
    }
    clearSort();
    if(sort_ascending){
        document.getElementById("headYear").innerHTML = "Year "+desc_span;
    }
    else{
        document.getElementById("headYear").innerHTML = "Year "+asc_span;
    }
    sortList();
}

function sortByVictories(){
    if(sort=="victorycount"){
        sort_ascending = !sort_ascending;
    }
    else{
        sort_ascending=false;
        sort="victorycount"
    }
    clearSort();
    if(sort_ascending){
        document.getElementById("headVictories").innerHTML = "Victories "+desc_span;
    }
    else{
        document.getElementById("headVictories").innerHTML = "Victories "+asc_span;
    }
    sortList();
}