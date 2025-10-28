function showTextInputPrompt(promptMessage, isPassword) {
    console.log("📝 Showing text input prompt:", promptMessage);
    
    $("#promptMessage").text(promptMessage);
    
    const inputField = $("#textInputField");
    inputField.val("");
    inputField.attr("type", isPassword ? "password" : "text");
    inputField.attr("placeholder", isPassword ? "Enter password..." : "Type here...");
    
    $("#textInputModal").fadeIn(300);
    
    setTimeout(() => {
        inputField.focus();
    }, 350);
    
    inputField.off('keypress').on('keypress', function(e) {
        if (e.which === 13) {
            submitTextInput();
        }
    });
}

function submitTextInput() {
    const inputValue = $("#textInputField").val().trim();
    
    if (!inputValue) {
        alert("Please enter a value");
        return;
    }
    
    console.log("✅ Submitting input");
    
    try {
        eel.submit_text_input(inputValue);
    } catch (error) {
        console.error("Error submitting input:", error);
    }
    
    $("#textInputField").val("");
    $("#textInputModal").fadeOut(300);
}

function cancelTextInput() {
    console.log("❌ Input cancelled");
    
    try {
        eel.submit_text_input(null);
    } catch (error) {
        console.error("Error cancelling input:", error);
    }
    
    $("#textInputField").val("");
    $("#textInputModal").fadeOut(300);
}

eel.expose(showTextInputPrompt);