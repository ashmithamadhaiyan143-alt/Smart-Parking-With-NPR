const video = document.getElementById("video");

if (video) {
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => video.srcObject = stream);
}

function capture() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 320;
    canvas.height = 240;

    ctx.drawImage(video, 0, 0, 320, 240);

    const img = canvas.toDataURL("image/jpeg",0.5);
    document.getElementById("imageInput").value = img;
}