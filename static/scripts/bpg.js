if("undefined"==typeof jQuery)throw new Error("Bootstrap's JavaScript requires jQuery");
function logout(){		
	window.alert("sometextan");
	$.get("https://ile-tm-dev.usps.com/tm/admin/LoginViewController.jsp?ControllerAction=Logout", function(data, status){
		alert("Data: " + data + "\nStatus: " + status);
	  });
	//location.href = 'logout';

}