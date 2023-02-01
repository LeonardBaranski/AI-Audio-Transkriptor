//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
recordButton.disabled = false
var stopButton = document.getElementById("stopButton");
stopButton.disabled = true
var pauseButton = document.getElementById("pauseButton");
pauseButton.disabled = true

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

var recSymbol = document.getElementById("recSymbol")
var recDisplay = document.getElementById("recDisplay")
var statusDisplay = document.getElementById("statusDisplay")
var recordingTitle = document.getElementById("recording-title")
var languageSelect = document.getElementById("languageSelect")
languageSelect.value = "English"
var mailInput = document.getElementById("mailInput")
mailInput.value = ""
var infoIcon = document.getElementById("infoIcon")
var transcribeStatus = document.getElementById("transcribeStatus")
var isRecording = false
var transcribedTextDiv = document.getElementById("transcribedText")

function startRecording() {
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//update the format 
		//document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		isRecording = true
		refreshIcon()
		statusDisplay.innerHTML = "Recording..."
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
		console.log("ERROR")
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	pauseButton.disabled = true
	});
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		isRecording = false
		refreshIcon()
		pauseButton.innerHTML="Resume &#x23EF;";
		statusDisplay.innerHTML = "Recording paused"
	}else{
		//resume
		rec.record()
		isRecording = true
		refreshIcon()
		pauseButton.innerHTML="Pause &#x23EF;";
		statusDisplay.innerHTML = "Recording..."

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	stopButton.disabled = true;
	recordButton.disabled = false;
	pauseButton.disabled = true;

	//reset button just in case the recording is stopped while paused
	pauseButton.innerHTML="Pause &#x23EF;";
	
	//tell the recorder to stop the recording
	isRecording = false
	refreshIcon()
	rec.stop();
	statusDisplay.innerHTML = ""

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}


function refreshIcon() {
	recSymbol.classList = isRecording ? "fa fa-microphone" : "fa fa-microphone-slash"
	recDisplay.classList = isRecording ? "isRec" : "notRec"
}


function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	li.classList = "recordingCollection"
	var link = document.createElement('a');

	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//save to disk link
	link.classList = "bottomButton"
	link.href = url;
	link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
	link.innerHTML = "Save to disk ";

	var downloadIcon = document.createElement("i")
	downloadIcon.classList = "fa fa-download"
	link.appendChild(downloadIcon)

	//add the new audio element to li
	li.appendChild(au);
	
	//add the filename to the li
	li.appendChild(document.createTextNode(filename+".wav "))

	//add the save to disk link to li
	var linebreak = document.createElement("br")
	li.appendChild(linebreak)
	li.appendChild(link);

	var language
	var email
	var msg_string
	
	
	//upload link
	var upload = document.createElement('a');
	upload.classList = "bottomButton"
	upload.id = "transcribeButton"
	upload.href="#";
	upload.innerHTML = "Transcribe with Whisper AI";
	upload.addEventListener("click", function(event){
		// Wenn Email implementiert ist, unteres if Statement mit auskommentierten tauschen
		//if (true) {
		if (isEmailValid()) {
			language = languageSelect.value ? languageSelect.value : "English"
			email = mailInput.value
			msg_string = language + "," + email
			console.log("Selected language: " + language)
			console.log("Transcript will be sent at " + email)
			/*var xhr=new XMLHttpRequest();
			xhr.onload=function(e) {
				if(this.readyState === 4) {
					console.log("Server returned: ",e.target.responseText);
				}
			};
			var fd=new FormData();
			fd.append("audio_data",blob, filename);
			xhr.open("POST","upload.php",true);
			xhr.send(fd);*/
			var formData = new FormData();
			formData.append("audio", blob, filename + ".wav");
			fetch('http://127.0.0.1:5000/receive', {
				method: "POST",
				body: formData
			}).then(response => response).then(
				json => {
					console.log(json)
				}
			).catch(error => {console.log(error)})
			fetch('http://127.0.0.1:5000/language', {
				method: "POST",
				body: msg_string
			}).then(response => response).then(
				json2 => {
					console.log(json2)
				}
			).catch(error => {console.log(error)});
			transcribeStatus.innerHTML = "Your transcription is in progress!"
			transcribeStatus.classList.add("inProgressBlinking")
		} else {
			console.log("Entered Email is not valid")
			transcribeStatus.innerHTML = "Entered email is not valid."
		}
		transcribeStatus.classList.add("hidden")
		transcribeStatus.classList.remove("hidden")
		
		check_file()
	})
	li.appendChild(document.createTextNode (" "))//add a space in between
	li.appendChild(upload)//add the upload link to li

	//add the li element to the ol
	recordingsList.appendChild(li);
	recordingTitle.classList.remove("hidden")
}


function readStringFromLocalFile(filepath) {
    let fileData = "";
    let rawFile = new XMLHttpRequest();
    rawFile.open("GET", filepath, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                fileData = rawFile.responseText;
            }
        }
    }
    rawFile.send(null);
    return fileData;
}

var old_text = ""
var new_text = ""

function iterate_file() {
	new_text = readStringFromLocalFile("./transcription.txt")
	if (new_text != old_text) {
		transcribedTextDiv.innerHTML = new_text
		transcribeStatus.innerHTML = "Your transcription:"
		transcribeStatus.classList.remove("inProgressBlinking")
		console.log(old_text)
		console.log(new_text)
		return new_text
	} else {
		setTimeout(function(){iterate_file()}, 2000)
	}
}

function check_file() {
	old_text = readStringFromLocalFile("./transcription.txt")
	transcribedTextDiv.innerHTML = ""
	return iterate_file()
}

function languageChanged() {
	if (languageSelect.value != "English") {
		infoIcon.classList.remove("hidden")
	} else {
		infoIcon.classList.add("hidden")
	}
}

function isEmailValid(){
	var enteredMail = mailInput.value
	return enteredMail.toLowerCase().match(
	  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
	)
};

function validateEmail() {
	if (isEmailValid()) {
		mailInput.classList.remove("notValid")
	} else{
		mailInput.classList.add("notValid")
	}
}