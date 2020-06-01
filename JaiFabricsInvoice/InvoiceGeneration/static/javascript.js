$('#printInvoice').click(function(){
           Popup($('.invoice')[0].outerHTML);
           function Popup(data)
           {
             console.log("HI")
               window.print();
               return true;
           }
       });


// alert("HI")
print()
