$(document).ready(function () {
  // Remove the eel.init()() - it's not needed here as Eel is already initialized by Python
  setTimeout(function() {
    eel.init()();  // This triggers the authentication and speech
  }, 1000);
  
  $(".text").textillate({
    loop: true,
    speed: 1500,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 940,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    height: 200,
    autostart: true,
    waveColor: "#ff0000",
    waveOffset: 0,
    rippleEffect: true,
    rippleColor: "#ffffff",
  });

  $("#MicBtn").click(async function () {
    try {
      // Use await for Eel calls for better error handling
      await eel.play_assistant_sound()();
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      await eel.takeAllCommands()();
    } catch (error) {
      console.error("Error in MicBtn click:", error);
    }
  });

  async function doc_keyUp(e) {
    if (e.key === "j" && e.metaKey) {
      try {
        await eel.play_assistant_sound()();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        await eel.takeAllCommands()();
      } catch (error) {
        console.error("Error in keyup:", error);
      }
    }
  }
  document.addEventListener("keyup", doc_keyUp, false);

  async function PlayAssistant(message) {
    if (message != "") {
      try {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        await eel.takeAllCommands(message)();  // Added ()() for proper Eel calling
        $("#chatbox").val("");
        $("#MicBtn").attr("hidden", false);
        $("#SendBtn").attr("hidden", true);
      } catch (error) {
        console.error("Error in PlayAssistant:", error);
        // Reset UI on error
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
      }
    } else {
      console.log("Empty message, nothing sent.");
    }
  }

  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      $("#MicBtn").attr("hidden", true);
      $("#SendBtn").attr("hidden", false);
    }
  }

  $("#chatbox").keyup(function () {
    let message = $("#chatbox").val();
    console.log("Current chatbox input: ", message);
    ShowHideButton(message);
  });

  $("#SendBtn").click(function () {
    let message = $("#chatbox").val();
    PlayAssistant(message);
  });

  $("#chatbox").keypress(function (e) {
    key = e.which;
    if (key == 13) {
      let message = $("#chatbox").val();
      PlayAssistant(message);
    }
  });
});