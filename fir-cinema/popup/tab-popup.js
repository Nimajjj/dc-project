/**
 * Listen for clicks on the buttons, and send the appropriate message to
 * the content script in the page.
 */
function listenForClicks() {
  document.addEventListener("click", (e) => {
    /**
     * Send a "scrap_page" message to the content script in the active tab.
     */
    function sendMessage(tabs) {
      browser.tabs.sendMessage(tabs[0].id, {
        command: "scrap_page",
      });
    }

    /**
     * Just log the error to the console.
     */
    function reportError(error) {
      console.error(`Could not scrap this page: ${error}`);
    }

    /**
     * Get the active tab, then call sendMessage() or reportError() as appropriate
     */
    if (e.target.tagName !== "BUTTON" || !e.target.closest("#popup-content")) {
      // Ignore when click is not on a button within <div id="popup-content">.
      return;
    }
    browser.tabs
      .query({ active: true, currentWindow: true })
      .then(sendMessage)
      .catch(reportError);
  });
}

/**
 * There was an error executing the script.
 * Display the popup's error message, and hide the normal UI.
 */
function reportExecuteScriptError(error) {
  document.querySelector("#popup-content").classList.add("hidden");
  document.querySelector("#error-content").classList.remove("hidden");
  console.error(`Failed to execute FirCinema content script: ${error.message}`);
}

/**
 * When the popup loads, inject a content script into the active tab,
 * and add a click handler.
 * If we couldn't inject the script, handle the error.
 */
browser.tabs
  .executeScript({ file: "/fir-cinema.js" })
  .then(listenForClicks)
  .catch(reportExecuteScriptError);
