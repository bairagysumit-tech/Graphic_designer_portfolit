$(document).ready(function(){
	var nav_btn = $(".nav_btn");
	var bar1 = $(".bar1");
	var bar2 = $(".bar2");
	var bar3 = $(".bar3");
	var mnb =  $(".mobile_nav_bar");
	nav_btn.click(function(){
		
		mnb.fadeIn(1000);
	});
	
	var mnb_c = $('.close_btn')
	
	mnb_c.click(function(){
		
		mnb.fadeOut(1000);
	});
});


$(window).resize(function(){
	var mnb =  $(".mobile_nav_bar");
  if ($(window).width() > 990) {
   mnb.css("display", "none");
}

});
