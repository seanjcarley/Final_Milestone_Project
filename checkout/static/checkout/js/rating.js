$(document).ready(function() {
    document.getElementById('star-1').addEventListener("click", function() {
        $('#star-1').addClass("checked");
        $('#star-2, #star-3, #star-4, #star-5').removeClass("checked");
        $('#id_rating').val(1);
    })
    document.getElementById('star-2').addEventListener("click", function() {
        $('#star-1, #star-2').addClass("checked");
        $('#star-3, #star-4, #star-5').removeClass("checked");
        $('#id_rating').val(2);
    })
    document.getElementById('star-3').addEventListener("click", function() {
        $('#star-1, #star-2, #star-3').addClass("checked");
        $('#star-4, #star-5').removeClass("checked");
        $('#id_rating').val(3);
    })
    document.getElementById('star-4').addEventListener("click", function() {
        $('#star-1, #star-2, #star-3, #star-4').addClass("checked");
        $('#star-5').removeClass("checked");
        $('#id_rating').val(4);
    })
    document.getElementById('star-5').addEventListener("click", function() {
        $('#star-1, #star-2, #star-3, #star-4, #star-5').addClass("checked");
        $('#id_rating').val(5);
    })
    document.getElementById('add').addEventListener("click", function() {
        $('#id_feedback').val(True);
    })
})