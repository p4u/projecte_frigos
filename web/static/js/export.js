var _canvas = null;

$(function() {
  $("#generate").on("click", function(e) {
    e.preventDefault();

    html2canvas($("#placeholder").get(0), {
      onrendered: function(canvas) {
        document.body.appendChild(canvas);
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1;
        var yyyy = today.getFullYear();
        var date = dd+'/'+mm+'/'+yyyy;
        var imgData = canvas.toDataURL('image/png');
        var doc = new jsPDF('landscape','pt');
        var w = 0;
        var max = 800;
        if (canvas.width > max) w = max;
        else w = canvas.width;
        var h = canvas.height * ( w/canvas.width );
        doc.text('Gràfica per aparell '+devname+' a data '+date, 20, 20);
        doc.addImage(imgData, 'PNG', 40, 60, w, h);
        doc.save('captura-'+devname+'.pdf');
      }
    });
  });
});
