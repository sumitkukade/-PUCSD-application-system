$( document ).ready(function() {

		$("#student-submit-button").click(function(){
				login();
		}); 
		$("#student-pin-validate-button").click(function(){
				validate_pin();
		}); 
		$("#get-student-code-button").click(function(){
				get_forget_otp();
		}); 
		$("#staff-submit-button").click(function(){
				staff_login();

		}); 
		$("#signup_pin_gen").click(function(){
				window.location = "signup.html";
		}); 
		$("#fill_information").click(function(){
				window.location = "signup.html";
		}); 
		$("#student-login-page").click(function(){
				window.location="login/student-login.html";	
		}); 
		$("#staff-login-page").click(function(){
				window.location="login/staff-login.html";	
		}); 
		$("#home-button").click(function(){
				window.location="../index.html";
		});
		$("#back-button").click(function(){
				window.location="../index.html";
		});
		$("#click-here").click(function(){
				window.location="login-successfull.html";
		});
		$("#already-have-pin-button").click(function(){
				window.location="forgot-password.html";
		});
		$("#login-page-button").click(function(){
				window.location="student-login.html";
		});
		$("#signup-button").click(function(){
				signup();
		});
		$("#validate-pin-button").click(function(){
				check_pin_for_signup();
		});

		$("#change-button").click(function(){
				change_student_filled_details();
		});


		var request = {}
		request["requestFor"] = "country";	
		$.post(
						location.protocol+"//"+window.location.hostname+"/index.py/get_country_names",
						{data: JSON.stringify(request)}

			  ).done(function(response) {
				//alert();
				var data = response.split(",");


				for(var i=0;i<data.length;i++)
				{
						var country = new Option(data[i].replace(/'/g,""));
						$("#country").append(country);	
				}
		});

			  $("#country").change(function () {
					  var countryName = this.value;
					  var request = {}
					  request["requestFor"] = "state";
					  request["countryName"] = countryName;
					  //alert(countryName);	

					  $.post(
									  location.protocol+"//"+window.location.hostname+"/index.py/get_country_names",
									  {data: JSON.stringify(request)}

							).done(function(response) {
							  // alert(response);
							  var data = response.split(",");

							  $("#state").empty();
							  for(var i=0;i<data.length;i++)
							  {
									  var country = new Option(data[i].replace(/'/g,""));
									  $("#state").append(country);
							  }
					  });


			  });


			  $("#state").change(function () {
					  var stateName = this.value;
					  var request = {}
					  request["requestFor"] = "city";
					  request["stateName"] = stateName;
					  //alert(stateName);	

					  $.post(
									  location.protocol+"//"+window.location.hostname+"/index.py/get_country_names",
									  {data: JSON.stringify(request)}

							).done(function(response) {

							  var data = response.split(",");
							  //alert(data);
							  $("#city").empty();
							  for(var i=0;i<data.length;i++)
							  {
									  var cityz = new Option(data[i].replace(/'/g,""));
									  $("#city").append(cityz);
							  }
					  });


			  });



			  // document.getElementById("date-band").innerHTML =  Date();

});

function deleteAllCookies() {
		var cookies = document.cookie.split(";");

		for (var i = 0; i < cookies.length; i++) {
				var cookie = cookies[i];
				var eqPos = cookie.indexOf("=");
				var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
				document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
		}
}




// this function is for get details of  
function get_student_filled_details(){
		// var roll_no = getCookie("roll_no");

		var roll_no = "16101";
		$('#rollno').val(roll_no);
		var request = {}
		request["rollno"] = $('#rollno').val();
		name = "submit"

				$.post(
								location.protocol+"//"+window.location.hostname+"/index.py/get_student_filled_details",
								{data: JSON.stringify(request)}

					  ).done(function(response) {
						//////////////////// incomplete
						console.log(response);
						response = JSON.parse(response);
						$('#fname').val(response["fname"]);
						$('#mname').val(response["mname"]);
						$('#lname').val(response["lname"]);
						if(response["gender"] == 'm'){$("#male").prop("checked", true)}
						if(response["gender"] == 'f'){$("#female").prop("checked", true)}
						$("#dob").val(response["dateOfBirth"]);
						$("#mob").val(response["contactNo"]);
						$("#email").val(response["email"]);
						if(response["courseId"] == 'mca'){$("#mca").prop("checked", true)}
						if(response["courseId"] == 'msc'){$("#msc").prop("checked", true)}

						////////////////// sem option select incomplete

						if(response["domicile"] == '1'){$("#domicileYes").prop("checked", true)}
						if(response["domicile"] == '0'){$("#domicileNo").prop("checked", true)}

						$("#category").val(response["category"]);
						$("#address-line-1").val(response["adderessLine1"]);
						$("#address-line-2").val(response["adderessLine2"]);
						$("#address-line-3").val(response["adderessLine3"]);
						$("#semId").val(response["semId"]);
						$("#country").val(response["countryId"]);
						$("#state").val(response["stateId"]);
						$("#city").val(response["cityId"]);

						////////////////// city country state select incomplete





				});


}


// Student edit details
function change_student_filled_details()
{
		if (document.getElementById('male').checked) {
				var gender = document.getElementById('male').value;
		}
		else if (document.getElementById('female').checked) {
				var gender = document.getElementById('female').value;
		}
		else if (document.getElementById('other').checked) {
				var gender = document.getElementById('other').value;
		}
		else{ status_msg("status-msg","please fill details: Gender"); return;}


		if (document.getElementById('mca').checked) {
				var courseId = document.getElementById('mca').value;
		}
		else if (document.getElementById('msc').checked) {
				var courseId = document.getElementById('msc').value;}
		else{status_msg("status-msg","please fill details: course"); return;}



		if (document.getElementById('domicileYes').checked) {
				var domicile = document.getElementById('domicileYes').value;
		}
		else if (document.getElementById('domicileNo').checked) {
				var domicile = document.getElementById('domicileNo').value;
		}
		else{ status_msg("status-msg","please fill details: domicile yes/no ??"); return;}


		var rollno = $("#rollno").val();
		var pin = $("#pin").val();
		var fname = $("#fname").val();
		var mname = $("#mname").val();
		var lname = $("#lname").val();
		var category = $("#category").val();
		var dob = $("#dob").val();
		var mobile = $("#mob").val();
		var email = $("#email").val();
		var semId = $("#semId").val();
		var address_line_1 = $("#address-line-1").val();
		var address_line_2 = $("#address-line-2").val();
		var address_line_3 = $("#address-line-3").val();
		var countryName = $("#country").val();
		var stateName = $("#state").val();
		var cityName = $("#city").val();

		var request = {};
		request["gender"] = gender;
		request["courseId"] = courseId;
		request["domicile"] = domicile;
		request["rollno"] = rollno;
		request["fname"] = fname;
		request["mname"] = mname;
		request["lname"] = lname;
		request["category"] = category;
		request["dob"] = dob;
		request["mobile"] = mobile;
		request["email"] = email;
		request["semId"] = semId;
		request["address_line_1"] = address_line_1;
		request["address_line_2"] = address_line_2;
		request["address_line_3"] = address_line_3;
		request["countryName"] = countryName;
		request["stateName"] = stateName;
		request["cityName"] = cityName;
		request["internationalStudentFlag"] = "";



		// extra international student information
		if (document.getElementById('intr').checked) 
		{
				var internationalStudentFlag = document.getElementById('intr').value;
				if(internationalStudentFlag != "")
				{
						var visaNumber = $("#international-visa").val();
						var visaType = $("#visaType").val();
						var visaDate = $("#visaIssueDate").val();
						var visaExpiryDate = $("#visaValidDate").val();
						var passportNumber = $("#passport-number").val();
						var admissionDate = $("#international-admission-date").val();
						var intCurrentAddressLine1 = $("#international-current-address-line-1").val();
						var intCurrentAddressLine2 = $("#international-current-address-line-2").val();
						var intCurrentAddressLine3 = $("#international-current-address-line-3").val();
						var passportDate = $("#passportIssueDate").val();
						var passportExpiryDate = $("#passportValidDate").val();
						var nationality = $("#nationality").val();


						request["visaNumber"] = visaNumber;
						request["visaType"] = visaType;
						request["visaDate"] = visaDate;
						request["visaExpiryDate"] = visaExpiryDate;
						request["passportNumber"] = passportNumber;
						request["admissionDate"] = admissionDate;
						request["intCurrentAddressLine1"] = intCurrentAddressLine1;
						request["intCurrentAddressLine2"] = intCurrentAddressLine2;
						request["intCurrentAddressLine3"] = intCurrentAddressLine3;
						request["passportIssuedOn"] = passportDate;
						request["passportValidTill"] = passportExpiryDate;
						request["nationality"] = nationality;
						request["internationalStudentFlag"] = internationalStudentFlag;
				}
		}
		$.post(

						location.protocol+"//"+window.location.hostname+"/index.py/change_student_filled_details",
						{data: JSON.stringify(request)}

			  ).done(function(response) {
				handle_response(response);
				////////////////////// incomplete
				alert("values changed");



		});





}



function check_pin_for_signup()
{
		var rollno = $("#rollno").val();
		var pin = $("#pin").val();
		var showFlag = false;
		var hiddeninputs = document.getElementsByClassName("hidden");
		var toDisable = []
				toDisable[0] = document.getElementById("validate-pin-button");
		toDisable[1] = document.getElementById("pin");
		toDisable[2] = document.getElementById("l1");

		request = {}
		request["roll_no"] = rollno;
		request["pin"] = pin;


		if(validate_roll_no(rollno) && validate_student_pin(pin)){
				$.post(
								location.protocol+"//"+window.location.hostname+"/index.py/is_valid_pin",
								{data: JSON.stringify(request)}

					  ).done(function(response) {
						if(response == "True")
						{
								showFlag = true;
								for(var i=0;i != hiddeninputs.length; i++){
										if(showFlag)
										{
												$("#rollno").attr("disabled", "disabled");
												for(var j = 0; j!=toDisable.length; j++)
												{
														toDisable[j].style.display = "none";	
												}

												hiddeninputs[i].style.display = "inline";
												status_msg("status-msg","");

										}
								}
						}
						else
						{
								status_msg("status-msg",response);
						}
				});
		}
}







/*session*/
function setCookie(cname, cvalue, exdays) {
		var d = new Date();
		d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
		var expires = "expires="+d.toUTCString();
		document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
		var name = cname + "=";
		var ca = document.cookie.split(';');
		for(var i = 0; i < ca.length; i++) {
				var c = ca[i];
				while (c.charAt(0) == ' ') {
						c = c.substring(1);
				}
				if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
				}
		}
		return "";
}

function login(){
		please_wait();
		var student_rollno = $("#student-rollno-input").val();
		var student_passwd = $("#student-password-input").val();

		var request = {};
		request["rollno"] = student_rollno;
		request["password"] = student_passwd;
		request["site-name"] = window.location.hostname;

				if(validate_roll_no(student_rollno) && validate_student_passwd(student_passwd)){
						/*alert(window.location.hostname);*/

						$.post(
										location.protocol+"//"+window.location.hostname+"/index.py/login",
										{data: JSON.stringify(request)}

							  ).done(function(response) {

								if (response == "True")
								{
										/*$.post(location.protocol+"//"+window.location.hostname+"/login/project_data/student.py",{data: JSON.stringify(request)}).done(function(response){alert(response)});*/
										setCookie("roll_no",student_rollno,3);
										//function to get IP
										$.getJSON("https://jsonip.com/?callback=?", function (data) {
												console.log(data);
												var ip = data.ip;
												setCookie("ip",ip,3)
										});

										window.location="project_data/stud_log.html";

										/*window.location="login-successfull.html";*/
								}
								else{
										status_msg('status-msg',response);
								}
						});

				}
				else{
						status_msg("status-msg","invalid rollno or password");
				}

}

function validate_roll_no(student_rollno)
{
		if(student_rollno == "")
		{
				status_msg('status-msg',"Please Enter Roll Number")
						return;
		}
		var re = /\d{5}/;
		var result = student_rollno.match(re);
		if(result == null)
		{
				status_msg('status-msg',"Invalid Roll Number");
				return false;
		}
		else{
				return true;
		}
}

function validate_student_passwd(student_passwd)
{
		if(student_passwd == "")
		{
				status_msg('status-msg',"Please Enter Password")
						return;
		}

		if(student_passwd.length<6)
		{
				status_msg('status-msg',"password length should be greater than 5");
				return false;
		}
		else
		{
				return true;
		}

}

function get_sha5(input_string){
		var sha5 = new jsSHA(input_string, "ASCII");
		return sha5.getHash("SHA-512", "HEX");
}

// function for if student forget their password
function validate_pin(){
		var student_rollno = $("#student-rollno-input").val();
		var student_pin = $("#student-pin-input").val();
		var student_pass = $("#student-password-input").val();
		var student_conf_pass = $("#student-confirm-password-input").val();
		if(student_pass != student_conf_pass)
		{
				status_msg("status-msg","password dosent match");
				return;
		}

		var request = {};
		request["roll_no"] = student_rollno;
		request["pin"] = student_pin;
		request["new_password"] = student_conf_pass;

		if(validate_roll_no(student_rollno) && validate_student_passwd(student_pass) && validate_student_pin(student_pin))
		{

				$.post(
								location.protocol+"//"+window.location.hostname+"/index.py/validate_pin",
								{data: JSON.stringify(request)}

					  ).done(function(response) {
						handle_response(response);
						if(response == "new_password,success")
						{								
								window.setTimeout(function(){

										window.location="student-login.html"
								}, 2500);
						}
				});

		}
		else{
				status_msg('status-msg',"invalid rollno or password");
		}

}


function signup(){
		please_wait();
		if (document.getElementById('male').checked) {
				var gender = document.getElementById('male').value;
		}
		else if (document.getElementById('female').checked) {
				var gender = document.getElementById('female').value;
		}
		else if (document.getElementById('other').checked) {
				var gender = document.getElementById('other').value;
		}
		else{ status_msg("status-msg","please fill details: Gender")}


		if (document.getElementById('mca').checked) {
				var courseId = document.getElementById('mca').value;
		}
		else if (document.getElementById('msc').checked) {
				var courseId = document.getElementById('msc').value;
		}

		else{status_msg("status-msg","please fill details: course")}


		if (document.getElementById('domicileYes').checked) {
				var domicile = document.getElementById('domicileYes').value;
		}
		else if (document.getElementById('domicileNo').checked) {
				var domicile = document.getElementById('domicileNo').value;
		}
		else{ status_msg("status-msg","please fill details: domicile yes/no ??")}


		var rollno = $("#rollno").val();
		var pin = $("#pin").val();
		var pwd = $("#pwd").val();
		var cpwd = $("#cpwd").val();
		var fname = $("#fname").val();
		var mname = $("#mname").val();
		var lname = $("#lname").val();
		var category = $("#category").val();
		var dob = $("#dob").val();
		var mobile = $("#mob").val();
		var email = $("#email").val();
		var semId = $("#semId").val();
		var address_line_1 = $("#address-line-1").val();
		var address_line_2 = $("#address-line-2").val();
		var address_line_3 = $("#address-line-3").val();
		var countryName = $("#country").val();
		var stateName = $("#state").val();
		var cityName = $("#city").val();

		if(pwd != cpwd)
		{
				status_msg("status-msg","password dosent match");
				return;
		}

		var request = {};
		request["gender"] = gender;
		request["courseId"] = courseId;
		request["domicile"] = domicile;
		request["rollno"] = rollno;
		request["pin"] = pin;
		request["pwd"] = cpwd;
		request["fname"] = fname;
		request["mname"] = mname;
		request["lname"] = lname;
		request["category"] = category;
		request["dob"] = dob;
		request["mobile"] = mobile;
		request["email"] = email;
		request["semId"] = semId;
		request["address_line_1"] = address_line_1;
		request["address_line_2"] = address_line_2;
		request["address_line_3"] = address_line_3;
		request["countryName"] = countryName;
		request["stateName"] = stateName;
		request["cityName"] = cityName;
		request["internationalStudentFlag"] = "";




		// extra international student information
		if (document.getElementById('intr').checked) {
				var internationalStudentFlag = document.getElementById('intr').value;
				if(internationalStudentFlag != "")
				{
						var visaNumber = $("#international-visa").val();
						var visaType = $("#visaType").val();
						var visaDate = $("#visaIssueDate").val();
						var visaExpiryDate = $("#visaValidDate").val();
						var passportNumber = $("#passport-number").val();
						var admissionDate = $("#international-admission-date").val();
						var intCurrentAddressLine1 = $("#international-current-address-line-1").val();
						var intCurrentAddressLine2 = $("#international-current-address-line-2").val();
						var intCurrentAddressLine3 = $("#international-current-address-line-3").val();
						var passportDate = $("#passportIssueDate").val();
						var passportExpiryDate = $("#passportValidDate").val();
						var nationality = $("#nationality").val();


						request["visaNumber"] = visaNumber;
						request["visaType"] = visaType;
						request["visaDate"] = visaDate;
						request["visaExpiryDate"] = visaExpiryDate;
						request["passportNumber"] = passportNumber;
						request["admissionDate"] = admissionDate;
						request["intCurrentAddressLine1"] = intCurrentAddressLine1;
						request["intCurrentAddressLine2"] = intCurrentAddressLine2;
						request["intCurrentAddressLine3"] = intCurrentAddressLine3;
						request["passportIssuedOn"] = passportDate;
						request["passportValidTill"] = passportExpiryDate;
						request["nationality"] = nationality;
						request["internationalStudentFlag"] = internationalStudentFlag;
				}
		}








		if(pwd != cpwd)
		{
				status_msg("status-msg","password and conform password NOT matched");
				return;
		}

		if(validate_roll_no(rollno) && validate_student_passwd(cpwd) && validate_student_pin(pin))
		{

				$.post(
								location.protocol+"//"+window.location.hostname+"/index.py/signup",
								{data: JSON.stringify(request)}

					  ).done(function(response) {
						alert(response);
						handle_response(response);
						if(response == "new_password,success")
						{
								status_msg("status-msg","&#x1f44d;  Information Submitted.");

								window.setTimeout(function(){
										window.location="information-submitted.html"
								}, 250);
						}
				});

		}
		else{
				status_msg('status-msg',"invalid");
		}

}



function validate_student_pin(pin)
{
		if(pin == "")
		{
				status_msg('status-msg',"Please Enter Pin")
						return;
		}
		var re = /\d{7}/;
		var result = pin.match(re);
		if(result == null)
		{
				status_msg('status-msg',"invalid pin");
				return false;
		}
		else{
				return true;
		}

}

function handle_response(response)
{
		result = response.split(',');
		if(result[0] == 'rollno')
		{
				if(result[1] == 'invalid')
				{
						status_msg('status-msg','invalid');
				}
		}
		else if(result[0] == 'pin')
		{
				if(result[1] == 'invalid')
						status_msg('status-msg','invalid pin');

		}
		else if(result[0] == 'new_password')
		{
				if(result[1] == 'success')
						status_msg('status-msg','New password set');
				//redirect to home page

		}

}
function status_msg(id,msg)
{
		document.getElementById(id).innerHTML = msg;
}

function forgot_password()
{
		request = {}
		var rollno = prompt("Please enter your roll no.", "");
		request["roll_no"] = rollno; 
		if (rollno != null)
		{
				if(validate_roll_no(rollno))
				{
						$.post(
										location.protocol+"//"+window.location.hostname+"/index.py/forgot_password",
										{data: JSON.stringify(request)}

							  ).done(function(response) {
								if(response == "True")
								{
										window.location="forgot-password-request-generated.html"

								}
						});
				}
		}
}

function get_forget_otp(){
		var rollno = $("#student-rollno-input").val();
		var request = {};
		request["rollno"] = rollno;
		$.post(
						location.protocol+"//"+window.location.hostname+"/index.py/get_student_reset_code",
						{data: JSON.stringify(request)}

			  ).done(function(response) {
				status_msg('status-msg',response);
				/*alert(response);*/
		});
}

function signup_pin(){
		request = {}
		var rollno = prompt("Please enter your roll no.", "");
		request["roll_no"] = rollno; 

		if (rollno != null)
		{
				if(validate_roll_no(rollno))
				{
						$.post(
										location.protocol+"//"+window.location.hostname+"/index.py/signup_pin_generator",
										{data: JSON.stringify(request)}

							  ).done(function(response) {
								if(response == "True")
								{
										window.location="signup-pin-generated.html"

								}
								else
								{
										alert("invalid user");
								}
						});
				}
		}
}

// function to print "please wait..." in status message
function please_wait()
{
		status_msg("status-msg","please wait...")
}



function staff_login(){
		please_wait();
		request = {}
		staff_username = $("#staff-input-username").val();
		staff_password = $("#staff-password-input").val();
		request["username"] = staff_username;
		request["password"] = staff_password;
		$.post(
						location.protocol+"//"+window.location.hostname+"/index.py/staff_login",
						{data: JSON.stringify(request)}

			  ).done(function(response) {
				if(response == "True")
				{
						/*$.post(location.protocol+"//"+window.location.hostname+"/project_data/staff.py/index",{data: JSON.stringify(request)}).done(function(response){alert(response);});*/
						/**/
						setCookie("staff-usernamee", staff_username, 3);
						//function to get IP
						$.getJSON("https://jsonip.com/?callback=?", function (data) {
								console.log(data);
								var ip = data.ip;
								setCookie("ip",ip,3)
						});


						window.location="project_data/staff_log.html";
						/*window.location="staff-login-successfull.html"*/
				}
				else
				{
						status_msg("status-msg",response);
				}
		});
}
function get_student_pin_link()
{
		window.location="staff-getApplication-code.html"
}
