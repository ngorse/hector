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
            message = $("#textInput").val().trim();
            if (!message) {
                return;
            }

            var userHtml = '<p class="userText"><span>' + message + "</span></p>";
            $("#textInput").val("");
            $("#chatbox").append(userHtml);
            refreshText();

            const data = { msg: message };
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                var botHtml = '<p class="botText"><span>' + data.response + "</span></p>";
                $("#chatbox").append(botHtml);
                refreshText();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        $(document).ready(function() {
            $("#textInput").keypress(function (e) {
                if (e.which == 13) {
                    getBotResponse();
                }
            });
        });