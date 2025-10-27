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

// ✅ STOP CONTINUOUS MODE
function stopContinuousMode() {
  try {
    eel.stop_assistant()();
    console.log("🛑 Continuous mode stopped");
  } catch (error) {
    console.error("Error:", error);
  }
}