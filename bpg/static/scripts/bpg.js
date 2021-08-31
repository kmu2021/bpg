if("undefined"==typeof jQuery)throw new Error("Bootstrap's JavaScript requires jQuery");
function logout(){		
	window.alert("Calling FA - Logout");
	  $.ajax({
		url: "https://ile-tm-dev.usps.com/tm/admin/LoginViewController.jsp?ControllerAction=Logout",
		type: "GET",
		success: (data, status, jqXHR) {
			window.alert(jqXHR.status);
		},
		error: function (error) {
		window.alert(error);
		}
		})
		window.alert("Calling BA - Logout");
		$.ajax({
			url: "https://ile-ba-dev.usps.com/ibmcognos/bi/v1/disp?b_action=xts.run&m=portal/logoff.xts&h_CAM_action=logoff",
			type: "GET",
			success: (data, status, jqXHR) {
				window.alert(jqXHR.status);
			},
			error: function (error) {
			window.alert(error);
			}
			})
	//location.href = 'logout';

}