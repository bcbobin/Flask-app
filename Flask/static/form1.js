var pass;
var filename;

$("input[type='submit']").on("click", function(){
	var username = document.querySelector("#name").value;
	pass = document.getElementById("password").value;
});





$("#fileUpload").change( function(){
	document.querySelector("#btnLabel").style.backgroundColor = "#aa272f";
	var file = document.querySelector("#fileUpload").files[0];
	var labelDis = document.querySelector("#fileUp");
	labelDis.textContent = this.files[0].name;
	filename = this.files[0].name;
});


