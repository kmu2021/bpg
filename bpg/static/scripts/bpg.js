if ("undefined" == typeof jQuery) throw new Error("Missing jQuery");

function logout() {
    console.log("Initiating Logout");
    for (i = 0; i < logoutUrls.length; i++) {
        console.log("Calling URL: " + logoutUrls[i]);
        $.ajax({
            url: logoutUrls[i],
            type: "GET",
            success: function(data, status, jqXHR) {
                console.log("Status: " + jqXHR.status);
            },
            error: function(error) {
                window.alert(error);
            }
        })
    }
    //location.href = 'logout';

}