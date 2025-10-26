$(document).ready(function () {
  // Display Speak Message
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    try {
      $(".siri-message li:first").text(message);
      $(".siri-message").textillate("start");
    } catch (error) {
      console.error("Error in DisplayMessage:", error);
    }
  }

  eel.expose(ShowHood);
  function ShowHood() {
    try {
      $("#Oval").attr("hidden", false);
      $("#SiriWave").attr("hidden", true);
    } catch (error) {
      console.error("Error in ShowHood:", error);
    }
  }

  eel.expose(senderText);
  function senderText(message) {
    try {
      var chatBox = document.getElementById("chat-canvas-body");
      if (message.trim() !== "") {
        chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`;

        chatBox.scrollTop = chatBox.scrollHeight;
      }
    } catch (error) {
      console.error("Error in senderText:", error);
    }
  }

  eel.expose(receiverText);
  function receiverText(message) {
    try {
      var chatBox = document.getElementById("chat-canvas-body");
      if (message.trim() !== "") {
        chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`;

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    } catch (error) {
      console.error("Error in receiverText:", error);
    }
  }

  eel.expose(hideLoader);
  function hideLoader() {
    try {
      $("#Loader").attr("hidden", true);
      $("#FaceAuth").attr("hidden", false);
    } catch (error) {
      console.error("Error in hideLoader:", error);
    }
  }

  // Hide Face auth and display Face Auth success animation
  eel.expose(hideFaceAuth);
  function hideFaceAuth() {
    try {
      $("#FaceAuth").attr("hidden", true);
      $("#FaceAuthSuccess").attr("hidden", false);
    } catch (error) {
      console.error("Error in hideFaceAuth:", error);
    }
  }

  // Hide success and display
  eel.expose(hideFaceAuthSuccess);
  function hideFaceAuthSuccess() {
    try {
      $("#FaceAuthSuccess").attr("hidden", true);
      $("#HelloGreet").attr("hidden", false);
    } catch (error) {
      console.error("Error in hideFaceAuthSuccess:", error);
    }
  }

  // Hide Start Page and display blob
  eel.expose(hideStart);
  function hideStart() {
    try {
      $("#Start").attr("hidden", true);

      setTimeout(function () {
        $("#Oval").addClass("animate__animated animate__zoomIn");
      }, 1000);
      setTimeout(function () {
        $("#Oval").attr("hidden", false);
      }, 1000);
    } catch (error) {
      console.error("Error in hideStart:", error);
    }
  }
});