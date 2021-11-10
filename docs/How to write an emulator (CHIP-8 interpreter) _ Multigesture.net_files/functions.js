$(document).ready(function() {



// Suckerfish



	$('ul.sf-menu').superfish({ 

		delay:       500,                             // delay on mouseout 

		animation:   {opacity:'show',height:'show'},  // fade-in and slide-down animation 

		speed:       'fast',                          // faster animation speed 

		autoArrows:  false,                           // disable generation of arrow mark-up 

		dropShadows: false                            // disable drop shadows 

	});

	

// jQuery Tabs

	

	$(".tab_content").hide(); //Hide all content

	$("ul.tabs li:first").addClass("active").show(); //Activate first tab

	$(".tab_content:first").show(); //Show first tab content



	//On Click Event

	$("ul.tabs li").click(function() {



		$("ul.tabs li").removeClass("active"); //Remove any "active" class

		$(this).addClass("active"); //Add "active" class to selected tab

		$(".tab_content").hide(); //Hide all tab content



		var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content

		$(activeTab).fadeIn(); //Fade in the active ID content

		return false;

	});


// jQuery Tabs

	

	$(".widget_tab_content").hide(); //Hide all content

	$("ul.widget-tabs li:first").addClass("active").show(); //Activate first tab

	$(".widget_tab_content:first").show(); //Show first tab content



	//On Click Event

	$("ul.widget-tabs li").click(function() {



		$("ul.widget-tabs li").removeClass("active"); //Remove any "active" class

		$(this).addClass("active"); //Add "active" class to selected tab

		$(".widget_tab_content").hide(); //Hide all tab content



		var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content

		$(activeTab).fadeIn(); //Fade in the active ID content

		return false;

	});


});