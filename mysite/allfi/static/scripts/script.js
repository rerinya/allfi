$(document).ready(function () {

    /*admin.html*/
    $("#but-info").click(function(){
        $(".info").show();
        $(".altauser").hide();
        $(".moduser").hide();
        $(".bajauser").hide();
        $(".subirpeli").hide();
        $(".modpeli").hide();
        $(".elimpeli").hide();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-info" ).attr("class", "list-group-item ac");
    });

    $("#but-alta").click(function(){
        $(".info").hide();
        $(".altauser").show();
        $(".moduser").hide();
        $(".bajauser").hide();
        $(".subirpeli").hide();
        $(".modpeli").hide();
        $(".elimpeli").hide();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-alta" ).attr("class", "list-group-item ac");
    });

    $("#but-mod").click(function(){
        $(".info").hide();
        $(".altauser").hide();
        $(".moduser").show();
        $(".bajauser").hide();
        $(".subirpeli").hide();
        $(".modpeli").hide();
        $(".elimpeli").hide();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-mod" ).attr("class", "list-group-item ac");
    });

    $("#but-baja").click(function(){
        $(".info").hide();
        $(".altauser").hide();
        $(".moduser").hide();
        $(".bajauser").show();
        $(".subirpeli").hide();
        $(".modpeli").hide();
        $(".elimpeli").hide();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-baja" ).attr("class", "list-group-item ac");
    });

    $("#but-pelisub").click(function(){
        $(".info").hide();
        $(".altauser").hide();
        $(".moduser").hide();
        $(".bajauser").hide();
        $(".subirpeli").show();
        $(".modpeli").hide();
        $(".elimpeli").hide();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-pelisub" ).attr("class", "list-group-item ac");
    });

    $("#but-pelimod").click(function(){
        $(".info").hide();
        $(".altauser").hide();
        $(".moduser").hide();
        $(".bajauser").hide();
        $(".subirpeli").hide();
        $(".modpeli").show();
        $(".elimpeli").hide();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-pelimod" ).attr("class", "list-group-item ac");
    });

    $("#but-pelieli").click(function(){
        $(".info").hide();
        $(".altauser").hide();
        $(".moduser").hide();
        $(".bajauser").hide();
        $(".subirpeli").hide();
        $(".modpeli").hide();
        $(".elimpeli").show();
        $(".mosuser").hide();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-pelieli" ).attr("class", "list-group-item ac");
    });

    $("#but-mostrar").click(function(){
        $(".info").hide();
        $(".altauser").hide();
        $(".moduser").hide();
        $(".bajauser").hide();
        $(".subirpeli").hide();
        $(".modpeli").hide();
        $(".elimpeli").hide();
        $(".mosuser").show();
        var name = document.getElementsByClassName("list-group-item ac");
        $(name).attr("class", "list-group-item");
        $( "#but-mostrar" ).attr("class", "list-group-item ac");
    });


    /*navbar*/
    var myNavBar = {
        elements: [],

        init: function (elements) {
            this.elements = elements;
        },

        add: function () {
            this.elements.forEach(function(elementId) {
                document.getElementById(elementId).classList.add('fixed-theme');
            })
        },

        remove: function () {
            this.elements.forEach(function(elementId) {
                document.getElementById(elementId).classList.remove('fixed-theme');
            })
        }
    };

     /*Init the object. Pass the object the array of elements
       that we want to change when the scroll goes down*/
    myNavBar.init([
        "header",
        "header-container",
        "brand"
    ]);

     /*Function that manage the direction
       of the scroll*/
    function offSetManager() {
        var yOffset = 0;
        var currYOffSet = window.pageYOffset;

        if (yOffset < currYOffSet) {
            myNavBar.add();
        }
        else if (currYOffSet == yOffset) {
            myNavBar.remove();
        }
    }

     /*bind to the document scroll detection*/
    window.onscroll = offSetManager;
     /*We have to do a first detectation of offset because the page
      could be load with scroll down set.*/
    offSetManager();


});


