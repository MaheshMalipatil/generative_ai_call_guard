function uploadAudio() {
    const fileInput = document.getElementById("audioInput");
    const resultDiv = document.getElementById("result");

    if (!fileInput.files || fileInput.files.length === 0) {
        resultDiv.innerText = "▲ Please select an audio file first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:8080/detect", {
        method: "POST",
        body: formData
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        // Handles both possible backend response shapes:
        // {label:..., confidence:...}  or  {result: {label:..., confidence:...}}
        if (data && data.label !== undefined && data.confidence !== undefined) {
            resultDiv.innerText =
                "Label: " + data.label + "\nConfidence: " + data.confidence;
        } else if (data && data.result && data.result.label !== undefined && data.result.confidence !== undefined) {
            resultDiv.innerText =
                "Label: " + data.result.label + "\nConfidence: " + data.result.confidence;
        } else {
            resultDiv.innerText = "Unexpected response from backend.";
        }
    })
    .catch(function (error) {
        console.error("Error:", error);
        resultDiv.innerText = "Error connecting to backend!";
    });
}