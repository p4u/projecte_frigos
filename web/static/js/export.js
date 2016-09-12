var _canvas = null;

$(function() {
  $("#generate").on("click", function(e) {
    e.preventDefault();

    html2canvas($("#placeholder").get(0), {
      onrendered: function(canvas) {
        document.body.appendChild(canvas);

        var imgData = canvas.toDataURL('image/png');
        var doc = new jsPDF('landscape');

        doc.addImage(imgData, 'PNG', 10, 10, 190, 95);
        doc.save('sample-file.pdf');
      }
    });
  });
});
