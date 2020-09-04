$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);
    
    var selectedVal = selector.val();
    
    if(selectedVal != "reset"){
        if (selectedVal == "img_title_asc") {
            var sort = "img_title";
            var direction = "asc";
        } else if (selectedVal == "img_title_desc") {
            var sort = "img_title";
            var direction = "desc";
        } else if (selectedVal == "img_rating_asc") {
            var sort = "img_rating";
            var direction = "asc";
        } else if (selectedVal == "img_rating_desc") {
            var sort = "img_rating";
            var direction = "desc";
        }else if (selectedVal == "base_price_asc") {
            var sort = "base_price";
            var direction = "asc";
        } else if (selectedVal == "base_price_desc") {
            var sort = "base_price";
            var direction = "desc";
        }
        
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
        
        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
        
        window.location.replace(currentUrl);
    }
})