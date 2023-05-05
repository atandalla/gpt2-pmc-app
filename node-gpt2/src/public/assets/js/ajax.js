// function graficar(event){
//     if(validar(event)){
//      $('#loadingmessage').show();
//      $('#boton').attr("disabled", true);
//      //Ocultar todo
//      $('#tablat,#container,#container1,#container2,#container3,#container4,#container5,#container7,#container8,#container9,#container10,#container11,#container12').hide();
//      $('#tablat tbody tr').remove();
//      vaciarPorcentaje();
//      $.ajax({
//          url:'/lit1',
//          data:{cant : $('#cantidad').val(),fechaInicio : $('#fechaInicio').val(),fechaFin : $('#fechaFin').val()},
//          type: 'POST',
       
//          success: function(msg){
//            $('#loadingmessage').hide();
//            $('#boton').attr("disabled", false);
 
//            $('#LDA').html('<object type="text/html" data="https://analisis-sentimiento.herokuapp.com/topic" style="width:120%;height:850px;"></object>');

//          },timeout : 9000000,
//          error :function(err){
//            $('#loadingmessage').hide();
//            $('#boton').attr("disabled", false);
//            console.log(err);
//            alert("Ha ocurrido un error");
//            }
//        })
//      }
//  }