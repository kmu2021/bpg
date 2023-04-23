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
    const firstname = document.querySelector('[name=firstName]').value;
    const lastname = document.querySelector('[name=lastName]').value;
    const workEmail = document.querySelector('[name=workEmail]').value;
    $.post("/getotp",
        {

            "csrfmiddlewaretoken": csrftoken,
            "workEmail": workEmail,
            "displayName": firstname + " " + lastname
        })
        .done(function (data, status) {
            //window.alert('status: ' + status + ', data: ' + data);
            if (status == "success") {
                otp = data;
                document.getElementById("resend-code").disabled = true;
                document.getElementById("error-twoFactorCode").textContent = data;
                //window.alert(otp);

            }
            else {
                document.getElementById("error-twoFactorCode").textContent = data;
                document.getElementById("resend-code").disabled = true;
            }
        })
        .fail(function (data, status) {
            console.log(data);
            document.getElementById("error-twoFactorCode").textContent = data.responseText;
            document.getElementById("resend-code").disabled = true;
        });

}

function resendCountDown() {// Get refreence to span and button
    var spn = document.getElementById("span-count");
    var btn = document.getElementById("resend-code");

    var count = 15;     // Set count
    var timer = null;  // For referencing the timer

    (function countDown() {
        // Display counter and start counting down
        spn.textContent = ' in ' + count + ' seconds';

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

function resendInvitation(firstname, lastname, workEmail, btnId) {
    $('#' + btnId).attr('disabled', true);
    $('#' + btnId).html('Resending');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.post("/resendinvitation",
        {

            "csrfmiddlewaretoken": csrftoken,
            "workEmail": workEmail,
            "firstName": firstname,
            "lastName": lastname
        })
        .done(function (data, status) {
            if (status == "success") {
                $("#resendInvitationModalBody").html(data);
                $('#resendInvitationModal').modal('show');
                $('#' + btnId).attr('disabled', false);
                $('#' + btnId).html('Resend Invitation');
            }
            else {
                $("#resendInvitationModalBody").html(data);
                $('#resendInvitationModal').modal('show');
                $('#' + btnId).attr('disabled', false);
                $('#' + btnId).html('Resend Invitation');
            }
        })
        .fail(function (data, status) {
            console.log(data);
            $('#' + btnId).attr('disabled', false);
            $('#' + btnId).html('Resend Invitation');
        });

}

function displayUserAccessControl(user_id, firstname, lastname, workEmail, invitationStatus) {
    $('#userAccessControlModalSubmit').removeClass('hidden');
    $('#userAccessControlModalClose').addClass('hidden');
    $('#pleaseWaitDialog').modal('show');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.get("/getuseraccesscontrolform",
        {

            "csrfmiddlewaretoken": csrftoken,
            "user_id": user_id,
            "workEmail": workEmail,
            "firstName": firstname,
            "lastName": lastname
        })
        .done(function (data, status) {
            if (status == "success") {
                $("#userAccessControlModalLabel").html('User: ' + firstname + ' ' + lastname);
                $("#userAccessControlModalBody").html(data);
                if (invitationStatus != "PendingAcceptance") {
                    $("[name='resendInvitationFlag']").attr("disabled", true);
                }
                $('<input>').attr('type', 'hidden').attr('name', 'modal_user_id').attr('value', user_id).attr('id', 'modal_user_id').appendTo('#userAccessControlModalBody');
                $('<input>').attr('type', 'hidden').attr('name', 'modal_first_name').attr('value', firstname).attr('id', 'modal_first_name').appendTo('#userAccessControlModalBody');
                $('<input>').attr('type', 'hidden').attr('name', 'modal_last_name').attr('value', lastname).attr('id', 'modal_last_name').appendTo('#userAccessControlModalBody');
                $('<input>').attr('type', 'hidden').attr('name', 'modal_work_email').attr('value', workEmail).attr('id', 'modal_work_email').appendTo('#userAccessControlModalBody');
                $('#pleaseWaitDialog').modal('hide');
                $('#userAccessControlModal').modal('show');
            }
            else {
                $("#userAccessControlModalBody").html(data);
                $('#pleaseWaitDialog').modal('hide');
                $('#userAccessControlModal').modal('show');
            }
        })
        .fail(function (data, status) {
            console.log(data);
        });

}


function saveUserAccessControl(user_id, first_name, last_name, work_email) {

    $('#pleaseWaitDialog').modal('show');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    frm = document.getElementById('userAccessControlForm');
    var frmData = new FormData(frm);
    frmData.append('csrfmiddlewaretoken', csrftoken);
    frmData.append('user_id', user_id);
    frmData.append('first_name', first_name);
    frmData.append('last_name', last_name);
    frmData.append('work_email', work_email);


    $.ajax({
        url: 'setuseraccesscontrolform',
        data: frmData,
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            $("#userAccessControlModalBody").html("User attributes have been updated. Please requery to see changes.");
            $('#pleaseWaitDialog').modal('hide');
            $('#userAccessControlModal').modal('show');
            $('#userAccessControlModalSubmit').addClass('hidden');
            $('#userAccessControlModalClose').removeClass('hidden');
        },
        error: function (err) {
            console.log(err);
            $("#userAccessControlModalBody").html("An Unexpected Error occured while granting access. Please Retry.");
            $('#pleaseWaitDialog').modal('hide');
            $('#userAccessControlModal').modal('show');
            $('#userAccessControlModalSubmit').addClass('hidden');
            $('#userAccessControlModalClose').removeClass('hidden');

        },
    });

}