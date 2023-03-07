if ("undefined" == typeof jQuery) throw new Error("Missing jQuery");

function logout() {
    console.log("Initiating Logout");
    try {
        for (i = 0; i < logoutUrls.length; i++) {
            console.log("Calling URL[" + i + "]: " + logoutUrls[i]);
            $.ajax({
                url: logoutUrls[i],
                type: "GET",
                async: false,
                cache: false,
                timeout: 30000,
                success: function (data, status, jqXHR) {
                    console.log("Status[" + i + "]: " + jqXHR.status);
                },
                error: function (error) {
                    console.log(error);
                }
            })
        }
    }
    catch (error) {
        console.log(error);
    }
    console.log("Redirecting to AAD Logout")
    location.href = 'logout';
}

function getOtp() {
    var otp;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.post("/getotp",
        {

            "csrfmiddlewaretoken": csrftoken
        },
        function (data, status) {
            if (status == "success") {
                otp = data;
                document.getElementById("resend-code").disabled=true;
                document.getElementById("error-twoFactorCode").textContent = "One Time Code has been sent";
                window.alert(otp);
                                
            }
        }
    );
}

function resendCountDown() {// Get refreence to span and button
    var spn = document.getElementById("span-count");
    var btn = document.getElementById("resend-code");

    var count = 15;     // Set count
    var timer = null;  // For referencing the timer

    (function countDown() {
        // Display counter and start counting down
        spn.textContent = ' in ' + count;

        // Run the function again every second if the count is not zero
        if (count !== 0) {
            timer = setTimeout(countDown, 1000);
            count--; // decrease the timer
        } else {
            // Enable the button
            btn.removeAttribute("disabled");
            spn.textContent = ''
        }
    }());
}