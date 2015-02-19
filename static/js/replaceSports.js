/**
 * Created by dmatt on 2/19/15.
 */

sports = {
    "Sport":"Sport",
    "mens-basketball":"MBB",
    "football":"FB",
    "baseball":"BB",
    "mens-lacrosse":"ML",
    "mens-soccer":"MS",
    "wrestling":"WR",
    "womens-basketball":"WBB",
    "field-hockey":"FH",
    "gymnastics":"GYM",
    "womens-lacrosse":"WL",
    "womens-soccer":"WS",
    "softball":"SB",
    "volleyball":"VB"
}

$(function(){
    console.log('Running ready')
    if ($(window).width() < 600) {
        console.log('width passes')
        $("td.sport").text(function(index,text){
            return sports[text];
        });
        $("thead .opponent").text('Team')
    }
});