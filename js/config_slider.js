/*----------nivoSlider----------*/

	$(window).load(function() {
	    $('#slider').nivoSlider({
	        effect: 'random', // Specify sets like: 'fold,fade,sliceDown'
	        slices: 15, // For slice animations
	        boxCols: 10, // For box animations
	        boxRows: 4, // For box animations
	        animSpeed: 500, // Slide transition speed
	        pauseTime: 4500, // How long each slide will show
	        startSlide: 0, // Set starting Slide (0 index)
	        directionNav: true, // Next & Prev navigation
	        directionNavHide: false, // Only show on hover
	        controlNav: true, // 1,2,3... navigation
	        controlNavThumbs: false, // Use thumbnails for Control Nav
	        controlNavThumbsFromRel: false, // Use image rel for thumbs
	        controlNavThumbsSearch: '.jpg', // Replace this with...
	        controlNavThumbsReplace: '_thumb.jpg', // ...this in thumb Image src
	        keyboardNav: true, // Use left & right arrows
	        pauseOnHover: true, // Stop animation while hovering
	        manualAdvance: false, // Force manual transitions
	        captionOpacity: 0.7, // Universal caption opacity
	        prevText: 'Prev', // Prev directionNav text
	        nextText: 'Next', // Next directionNav text
	        beforeChange: function(){}, // Triggers before a slide transition
	        afterChange: function(){}, // Triggers after a slide transition
	        slideshowEnd: function(){}, // Triggers after all slides have been shown
	        lastSlide: function(){}, // Triggers when last slide is shown
	        afterLoad: function(){} // Triggers when slider has loaded
	    });    
	});

/*----------dropmenu----------*/

	jQuery(document).ready(function() {
	jQuery("#dropmenu ul").css({display: "none"}); // Opera Fix
	jQuery("#dropmenu li").hover(function(){
			jQuery(this).find('ul:first').css({visibility: "visible",display: "none"}).show(268);
			},function(){
			jQuery(this).find('ul:first').css({visibility: "hidden"});
			});
	});
	
