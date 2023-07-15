$(document).ready(function() {
    $("form").submit(function(event) {
        event.preventDefault(); // Prevent form submission

        var fileInput = document.getElementById("imageInput");
        var file = fileInput.files[0];

        var formData = new FormData();
        formData.append("file", file);

        $.ajax({
            url: "http://localhost:8000/predict",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var resultElement = document.getElementById("result");
                resultElement.innerHTML = "Predicted game: " + response.result;

                var recommendationsElement = document.getElementById("recommendations");
                recommendationsElement.innerHTML = "";

                for (var i = 0; i < response.recommendations.length; i++) {
                    var game = response.recommendations[i];
                    var gameElement = document.createElement("div");
                    gameElement.innerHTML = "<h3>" + game.game_title + "</h3>" +
                        "<p>" + game.plot + "</p>" +
                        "<a href='" + game.url + "' target='_blank'>View more</a>";
                    recommendationsElement.appendChild(gameElement);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    // Display the selected image
    $("#imageInput").change(function() {
        var file = $(this)[0].files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var img = new Image();
                img.src = e.target.result;
                img.onload = function() {
                    var canvas = document.createElement("canvas");
                    var ctx = canvas.getContext("2d");
                    var maxSize = 200; // Maximum size of the square box

                    var width = this.width;
                    var height = this.height;

                    if (width > height) {
                        if (width > maxSize) {
                            height *= maxSize / width;
                            width = maxSize;
                        }
                    } else {
                        if (height > maxSize) {
                            width *= maxSize / height;
                            height = maxSize;
                        }
                    }

                    canvas.width = width;
                    canvas.height = height;

                    ctx.drawImage(this, 0, 0, width, height);
                    var resizedDataUrl = canvas.toDataURL("image/jpeg");
                    $("#selectedImage").attr("src", resizedDataUrl);
                    $("#uploadText").hide();
                };
            };
            reader.readAsDataURL(file);
        } else {
            $("#selectedImage").attr("src", "");
            $("#uploadText").show();
        }
    });
});
