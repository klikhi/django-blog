var logocolor="white";
var navcolor="blue2";
var sidecolor="white";
var bgcolor="bg1";




function savecookie(g){

current=g.className;
if(current == "changeTopBarColor" || current=="selected changeTopBarColor")
{
    navcolor=g.getAttribute('data-color');

}
else if(current == "changeLogoHeaderColor" || current=="selected changeLogoHeaderColor")
{
    logocolor = g.getAttribute('data-color');
}
else if( current=="selected changeSideBarColor" || current =="changeSideBarColor")
{
    sidecolor= g.getAttribute('data-color');
}
else if(current = "changeBackgroundColor selected" || current == "changeBackgroundColor")
{
    bgcolor= g.getAttribute('data-color');
}
document.cookie="";
var now = new Date();
now.setTime(now.getTime() + 5*365*30*24 * 3600 * 1000);
expire=now.toUTCString();
document.cookie="colors="+logocolor+"&"+navcolor+"&"+sidecolor+"&"+bgcolor+";"+"expires="+expire+";";
console.log(document.cookie);

}

loadcookie();

function loadcookie()
{
    
try
{clogocolor=document.cookie.split(';')[1].split('=')[1].split('&')[0];
cnavcolor=document.cookie.split(';')[1].split('=')[1].split('&')[1];
csidecolor=document.cookie.split(';')[1].split('=')[1].split('&')[2];
cbgcolor=document.cookie.split(';')[1].split('=')[1].split('&')[3];
logocolor=clogocolor;
navcolor =cnavcolor;
sidecolor= csidecolor;
bgcolor=cbgcolor;
document.getElementById("logo").setAttribute('data-background-color',clogocolor);
document.getElementById("navbar").setAttribute('data-background-color',cnavcolor);
document.getElementById("sidebar").setAttribute('data-background-color',csidecolor);
document.getElementById("body").setAttribute('data-background-color',cbgcolor);
document.cookie="";
}
catch{
console.log("No cookie saved until now");
}}