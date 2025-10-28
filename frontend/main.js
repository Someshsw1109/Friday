// ✅ GLOBAL STATE
let isListening = false;

$(document).ready(function () {
  setTimeout(function() {
    eel.init()();
  }, 1000);
  
  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: { effect: "fadeInUp", sync: true },
    out: { effect: "fadeOutUp", sync: true },
  });

  // ✅ TEXT INPUT
  async function PlayAssistant(message) {
    if (message != "") {
      try {
        await eel.takeAllCommands(message)();
        $("#chatbox").val("");
        $("#SendBtn").attr("hidden", true);
      } catch (error) {
        console.error("Error:", error);
      }
    }
  }

  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#SendBtn").attr("hidden", true);
    } else {
      $("#SendBtn").attr("hidden", false);
    }
  }

  $("#chatbox").keyup(function () {
    let message = $("#chatbox").val();
    ShowHideButton(message);
  });

  $("#SendBtn").click(function () {
    let message = $("#chatbox").val();
    PlayAssistant(message);
  });

  $("#chatbox").keypress(function (e) {
    if (e.which == 13) {
      let message = $("#chatbox").val();
      PlayAssistant(message);
    }
  });
});

// ✅ TOGGLE ASSISTANT (START/STOP)
function toggleAssistant() {
  if (isListening) {
    // Stop listening
    stopContinuousMode();
  } else {
    // Start listening
    startContinuousMode();
  }
}

// ✅ START CONTINUOUS MODE
function startContinuousMode() {
  try {
    console.log("🚀 Starting continuous mode...");
    eel.start_assistant()();
    isListening = true;
    
    // Update button
    $("#toggleBtn").removeClass("control-btn-start").addClass("control-btn-stop");
    $("#toggleBtn i").removeClass("bi-play-circle").addClass("bi-stop-circle");
    $("#toggleBtnText").text("Stop Listening");
    
  } catch (error) {
    console.error("Error starting:", error);
  }
}

// ✅ STOP CONTINUOUS MODE
function stopContinuousMode() {
  try {
    console.log("🛑 Stopping continuous mode...");
    eel.stop_assistant()();
    isListening = false;
    
    // Update button
    $("#toggleBtn").removeClass("control-btn-stop").addClass("control-btn-start");
    $("#toggleBtn i").removeClass("bi-stop-circle").addClass("bi-play-circle");
    $("#toggleBtnText").text("Start Listening");
    
  } catch (error) {
    console.error("Error stopping:", error);
  }
}