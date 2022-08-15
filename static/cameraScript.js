(() => {
    // The width and height of the captured photo. We will set the
    // width to the value defined here, but the height will be
    // calculated based on the aspect ratio of the input stream.

    const width = 320; // We will scale the photo width to this
    let height = 0; // This will be computed based on the input stream

    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.

    let streaming = false;

    // The various HTML elements we need to configure or control. These
    // will be set by the startup() function.

    let video = null;
    let canvas = null;
    let photo = null;

    function showViewLiveResultButton() {
        if (window.self !== window.top) {
            document.querySelector(".contentarea").remove();
            const button = document.createElement("button");
            button.textContent = "View live result of the example code above";
            document.body.append(button);
            button.addEventListener('click', () => window.open(location.href));
            return true;
        }
        return false;
    }

    async function startup() {
        if (showViewLiveResultButton()) { return; }
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');

        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then((stream) => {
                video.srcObject = stream;
                video.play();
            })
            .catch((err) => {
                console.error(`An error occurred: ${err}`);
            });

        video.addEventListener('canplay', (ev) => {
            if (!streaming) {
                height = video.videoHeight / (video.videoWidth / width);

                // Firefox currently has a bug where the height can't be read from
                // the video, so we will make assumptions if this happens.

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAttribute('width', width);
                video.setAttribute('height', height);
                canvas.setAttribute('width', width);
                canvas.setAttribute('height', height);
                streaming = true;
            }
        }, false);
        while (true) {
            await sleep(5);
            takepicture();
        }
    }

    function sleep(sec) {
        sec *= 1000;
        return new Promise(resolve => setTimeout(resolve, sec));
    }

    function takepicture() {
        const context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            const data = canvas.toDataURL('image/png');
            callAPI(data);
        }
    }

    function callAPI(data) {
        let body = new FormData();
        body.append("upload", data);
        // Or body.append('upload', base64Image);
        body.append("regions", "IL"); // Change to your country
        fetch("https://api.platerecognizer.com/v1/plate-reader/", {
            method: "POST",
            headers: {
                Authorization: "Token 719fadfc3ca6e38f30fb4d09a15542e2b599af99",
            },
            body: body,
        })
            .then((res) => res.json())
            .then((json) => stateChanger(json))
            .catch((err) => {
                console.log(err);
            });
    }

    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener('load', startup, false);
})();