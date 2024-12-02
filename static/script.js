        function toggleWaitIndicators() {
            var button = document.getElementById("sendButton");
            button.disabled = !button.disabled;
            var wheel = document.getElementById("running");
            wheel.style.display = (wheel.style.display === 'none') ? 'flex' : 'none';
        }

        function refreshText() {
            document
               .getElementById("textInput")
               .scrollIntoView({ block: "start", behavior: "smooth" });
            var div = document.getElementById("chatbox");
            div.scrollTop = div.scrollHeight;
            toggleWaitIndicators();
        }

        function getBotResponse() {
            if ($("#textInput").val().length == 0) {
                return;
            }
            var rawText = $("#textInput").val();
            var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
            $("#textInput").val("");
            $("#chatbox").append(userHtml);
            refreshText();
            $.get("/get", { msg: rawText }).done(function (data) {
                var botHtml = '<p class="botText"><span>' + data + "</span></p>";
                $("#chatbox").append(botHtml);
                refreshText();
            });
        }

        $("#textInput").keypress(function (e) {
            if (e.which == 13) {
                getBotResponse();
            }
        });
