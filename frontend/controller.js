$(document).ready(function () {
  
  // ✅ DISPLAY MESSAGE
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    try {
      $(".siri-message li:first").text(message);
      $(".siri-message").textillate("start");
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // ✅ UPDATE STATUS INDICATOR
  eel.expose(updateStatus);
  function updateStatus(status) {
    const indicator = $("#status-indicator");
    const text = $("#status-text");
    
    indicator.removeClass("status-inactive status-active status-processing");
    
    if (status === "listening") {
      indicator.addClass("status-active");
      text.text("LISTENING");
    } else if (status === "processing") {
      indicator.addClass("status-processing");
      text.text("PROCESSING");
    } else {
      indicator.addClass("status-inactive");
      text.text("STANDBY");
    }
  }

  // ✅ ENABLE CONTINUOUS MODE UI
  eel.expose(enableContinuousMode);
  function enableContinuousMode() {
    $("#listening-mode").fadeIn();
    $("#stopBtn").fadeIn();
  }

  // ✅ DISABLE CONTINUOUS MODE UI
  eel.expose(disableContinuousMode);
  function disableContinuousMode() {
    $("#listening-mode").fadeOut();
    $("#stopBtn").fadeOut();
  }

  // ✅ SENDER TEXT
  eel.expose(senderText);
  function senderText(message) {
    try {
      var chatBox = document.getElementById("chat-canvas-body");
      if (chatBox && message.trim() !== "") {
        chatBox.innerHTML += `<div class="row justify-content-end mb-4">
          <div class="width-size">
            <div class="sender_message">${message}</div>
          </div>
        </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // ✅ RECEIVER TEXT
  eel.expose(receiverText);
  function receiverText(message) {
    try {
      var chatBox = document.getElementById("chat-canvas-body");
      if (chatBox && message.trim() !== "") {
        chatBox.innerHTML += `<div class="row justify-content-start mb-4">
          <div class="width-size">
            <div class="receiver_message">${message}</div>
          </div>
        </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  eel.expose(hideLoader);
  function hideLoader() {
    $("#Loader").attr("hidden", true);
    $("#FaceAuth").attr("hidden", false);
  }

  eel.expose(hideFaceAuth);
  function hideFaceAuth() {
    $("#FaceAuth").attr("hidden", true);
    $("#FaceAuthSuccess").attr("hidden", false);
  }

  eel.expose(hideFaceAuthSuccess);
  function hideFaceAuthSuccess() {
    $("#FaceAuthSuccess").attr("hidden", true);
    $("#HelloGreet").attr("hidden", false);
  }

  eel.expose(hideStart);
  function hideStart() {
    $("#Start").attr("hidden", true);
    setTimeout(function () {
      $("#Oval").attr("hidden", false);
    }, 1000);
  }
});