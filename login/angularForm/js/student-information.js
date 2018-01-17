$( document ).ready(function() {
		$("#validate-pin-button").click(function(){
				/*var isValidPin = validate_pin();*/
		});
		$("#signup-button").click(function(){
				submit_student_details();
		});
});



function submit_student_details(){

if (document.getElementById('male').checked) {
  var gander = document.getElementById('male').value;
}
else if (document.getElementById('female').checked) {
  var gander = document.getElementById('female').value;
}
else if (document.getElementById('other').checked) {
  var gander = document.getElementById('other').value;
}
else{ console.log("please fill details: Gander")}


if (document.getElementById('mca').checked) {
  var courseId = document.getElementById('mca').value;
}
else if (document.getElementById('msc').checked) {
  var courseId = document.getElementById('msc').value;
}
else if (document.getElementById('mtech').checked) {
  var courseId = document.getElementById('mtech').value;
}
else{ console.log("please fill details: course")}


alert(courseId);

if (document.getElementById('domicileYes').checked) {
  var domicile = document.getElementById('domicileYes').value;
}
else if (document.getElementById('domicileNo').checked) {
  var domicile = document.getElementById('domicileNo').value;
}
else{ console.log("please fill details: domicile")}	

	var rollno = $("#rollno").val();
	var pin = $("#pin").val();
	var pwd = $("#pwd").val();
	var cpwd = $("#pwd").val();
	var name = $("#name").val();
	var category = $("#category").val();
	var dob = $("#dob").val();
	var mobile = $("#mob").val();
	var email = $("#email").val();
	var sem = $("#sem").val();
	var address = $("#address").val();
}