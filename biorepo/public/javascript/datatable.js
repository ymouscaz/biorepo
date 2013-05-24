
$(document).ready(function() {
    /* Add a click handler to the rows - this could be used as a callback */
    $('.grid tbody tr').click( function() {
        if ( $(this).hasClass('row_selected') )
            $(this).removeClass('row_selected');
        else
            $(this).addClass('row_selected');

    });

    $('div.buttons').submit( function() {
        var sData = $('input', oTable.fnGetNodes()).serialize();
        alert( "The following data would have been submitted to the server: \n\n"+sData );
        return false;}
    );

    /* Init the table */
    var searchlists = $.parseJSON($('#searchlists').html());
    var oTable = $('.grid').dataTable( {
        "aoColumnDefs": [{ "bVisible": false, "aTargets": searchlists[0] }], /* trono : 7 * aTargerts == hidden but searchable aTargets == hidden_positions*/
        "sDom": 'Wlfriptip',
        bPaginate: true,
        "oColumnFilterWidgets": {
            sSeparator: "\\s*;+\\s*",
            "aiExclude": searchlists[1],  /* exclude "action column trono" research bouton field example : "aiExclude" == positions_not_searchable */
            /*"aiExclude" : [10,13],*/
            "sPaginationType": "full_numbers"
        }
    });



    /* $('.row_selected') */
    /* customize interface searchpage*/
    $('.dataTables_info').first().remove();
    /*$('.dataTables_paginate').first().remove();*/
    $('.paging_two_button').first().remove();

    /* Actions buttons */
    /* DOWNLOAD BUTTON */
    // var dlButton = document.createElement("input");
    // dlButton.name ="dl";
    // dlButton.type = "submit";
    // dlButton.value ="Download";
    // console.log(XMLHttpRequest);
    // $(dlButton).click(function(){
    //     alert("Multi download button is not yet available");
    //     $.ajax({
    //         type: 'POST',
    //         url: "http://localhost:8080/biorepo/measurements/new",
    //         data: "meas_id="+getListIdSelected(),

    //         success: new XMLHttpRequest().getResponseHeader("Location")

    //     });

    //     return false;

    // });

    var createForm = document.createElement("form");
    createForm.id="form";


    //get the selected measurement IDs onClick
    $(createForm).submit(function(e) {
       var m = getListIdSelected();
       return m, false;
    });

    /* UCSC BUTTON */
    // var ucscButton = document.createElement("input");
    // ucscButton.name = "ucsc";
    // ucscButton.type = "submit";
    // ucscButton.value ="view in UCSC";
    // $(ucscButton).click(function(){
    //     alert("UCSC visualisation button is not yet available");
    //     var measUCSC = getListIdSelected();
    //     console.log(measUCSC);
    //     $.ajax({
    //         type:'POST',
    //         url: "http://localhost:8080/biorepo/measurements/UCSC",
    //         data : "meas_id="+measUCSC

    //     });

    // });
    /* ucscButton.onClick(); */

    /* GDV BUTTON */
    // var gdvButton = document.createElement("input");
    // gdvButton.name = "gdv";
    // gdvButton.type = "submit";
    // gdvButton.value ="view in GDV";
    // $(gdvButton).click(function(){
    //     alert("GDV visualisation button is not yet available");
    // });
    /* gdvButton.onClick(); */

    /* UPLOAD CHILD BUTTON */
    var upButton = document.createElement("input");
    upButton.name = "upload";
    upButton.type = "submit";
    upButton.value = "Create new measurement from selected";

    $(upButton).click(function(){
        var meas = getListIdSelected();

        document.body.innerHTML+='<form id="formtemp" action="http://localhost:8080/biorepo/measurements/new" method="POST">' +
            '<input id="parents" name="parents" type="hidden" value="' + meas + '"/></form>';
        document.getElementById("formtemp").submit();
    });






    var createDiv = document.createElement("div");
    var createDiv2 = document.createElement("div");
    createDiv.className="buttons";
    createDiv.textContent = "Possible action for selected rows : ";
    createDiv2.className="dataTables_buttons";

    createDiv2.appendChild(createForm);
    createForm.appendChild(createDiv);
    //createDiv.appendChild(dlButton);
    //createDiv.appendChild(ucscButton);
    //createDiv.appendChild(gdvButton);
    createDiv.appendChild(upButton);
    $(createDiv2).insertAfter('.dataTables_filter');

    // TODO : loading on click dl
    // $('.dl_link').each(function(i,e){
    // var h = $(this).attr("href");
    // $(this).attr("href","#");
    // var path_img = "./biorepo/public/images/dna_loader.gif";
    // $(this).click(function(){
    // //display.image
    // });
    // });

} );

function getListIdSelected()
{
    var listID = [];
    $('.row_selected').children().find('.id_meas').each(function(i){
        listID[i]=$(this).text();
    });

    if (listID.length !== 0){
        return listID;
    }
    else{
        return null;
    }
}
