// POC - HTTP Connection from Indesign via ExtendScript to a FastAPI backend running locally on http://127.0.0.1:8000

// Debug function for the ExtendScript console
function log(message) {
    $.writeln("DEBUG: " + message);
}

// Function to properly encode special characters in URLs
function encodeURIComponent(str) {
    return encodeURI(str).replace(/[!'()*]/g, function(c) {
        return '%' + c.charCodeAt(0).toString(16);
    });
}

// Create a basic UI
var dialog = new Window("dialog", "FastAPI Connection Tool");
dialog.orientation = "column";
dialog.alignChildren = ["fill", "top"];
dialog.preferredSize.width = 500;
dialog.preferredSize.height = 800;

// Settings panel
var settingsPanel = dialog.add("panel", undefined, "Connection Settings");
settingsPanel.orientation = "column";
settingsPanel.alignChildren = ["left", "top"];
settingsPanel.margins = 20;

// Host settings
var hostGroup = settingsPanel.add("group");
hostGroup.add("statictext", undefined, "Host:").preferredSize.width = 80;
var hostInput = hostGroup.add("edittext", undefined, "127.0.0.1");
hostInput.characters = 15;
hostGroup.add("statictext", undefined, "Port:");
var portInput = hostGroup.add("edittext", undefined, "8000");
portInput.characters = 5;

// Path setting
var pathGroup = settingsPanel.add("group");
pathGroup.add("statictext", undefined, "Path:").preferredSize.width = 80;
var pathInput = pathGroup.add("edittext", undefined, "/get_layer_config?configName=default");
pathInput.characters = 40;

// Format options
var formatGroup = settingsPanel.add("group");
formatGroup.add("statictext", undefined, "Format:").preferredSize.width = 80;
var formatDropdown = formatGroup.add("dropdownlist", undefined, ["Standard HTTP/1.1", "Minimal HTTP/1.1", "Raw Test"]);
formatDropdown.selection = 0;

// Add a checkbox for debug mode
var debugGroup = settingsPanel.add("group");
var debugCheck = debugGroup.add("checkbox", undefined, "Show sent request in results");

// Buttons
var buttonGroup = dialog.add("group");
buttonGroup.alignment = ["center", "top"];
var testButton = buttonGroup.add("button", undefined, "Test Connection");
// var copyButton = buttonGroup.add("button", undefined, "Copy Results");

// Results
var resultsPanel = dialog.add("panel", undefined, "Results");
resultsPanel.orientation = "column";
resultsPanel.alignChildren = ["fill", "fill"];
var resultsText = resultsPanel.add("edittext", undefined, "", {multiline: true, scrollable: true});
resultsText.preferredSize.height = 300;

// Status
var statusText = dialog.add("statictext", undefined, "Ready");


// Execute the API test
testButton.onClick = function() {
    try {
        statusText.text = "Testing connection...";
        resultsText.text = "Connecting...";
        
        // Get values from UI
        var host = hostInput.text;
        var port = portInput.text;
        var path = pathInput.text;
        var format = formatDropdown.selection.index;
        var showDebug = debugCheck.value;
        
        // Ensure path starts with a slash
        if (path.charAt(0) !== "/") {
            path = "/" + path;
        }
        
        // Log what we're doing
        log("Testing connection to " + host + ":" + port + path);
        
        // Create socket
        var conn = new Socket();
        var result = "";
        
        if (conn.open(host + ":" + port)) {
            // Build request based on format
            var request;
            
            if (format === 0) { // Standard HTTP/1.1
                request = "GET " + path + " HTTP/1.1\r\n";
                request += "Host: " + host + (port != "80" ? ":" + port : "") + "\r\n";
                request += "User-Agent: InDesign/APIDebugTool\r\n";
                request += "Accept: */*\r\n";
                request += "Connection: close\r\n\r\n";
            } 
            else if (format === 1) { // Minimal HTTP/1.1
                request = "GET " + path + " HTTP/1.1\r\n";
                request += "Host: " + host + (port != "80" ? ":" + port : "") + "\r\n\r\n";
            }
            else { // Raw Test - absolute minimum HTTP request
                request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n";
            }
            
            // Log the exact request being sent, with visible line endings
            log("Sending exact bytes: " + request.replace(/\r/g, "\\r").replace(/\n/g, "\\n"));
            
            // Send the request - ensure binary encoding
            conn.encoding = "binary"; // Ensure binary mode
            conn.write(request);
            
            // If debug is enabled, show the request in the results
            var displayResult = "";
            if (showDebug) {
                displayResult = "--- REQUEST SENT ---\n" + 
                               request.replace(/\r\n/g, "\n") + 
                               "\n--- RESPONSE ---\n";
            }
            
            // Read the response
            log("Reading response...");
            
            // Set a timeout for reading
            var startTime = new Date().getTime();
            var timeout = 5000; // 5 seconds timeout
            
            // Read data until socket is closed or timeout
            while (!conn.eof) {
                var chunk = conn.read(1024);
                if (chunk) {
                    result += chunk;
                }
                
                // Check for timeout
                if (new Date().getTime() - startTime > timeout) {
                    log("Timeout reading response");
                    break;
                }
                
                // Small delay to prevent high CPU usage
                $.sleep(10);
            }
            
            log("Response received, length: " + result.length);
            
            // Close the connection
            conn.close();
            
            // Show the result
            resultsText.text = displayResult + result;
            statusText.text = "Connection successful";
            
            // Check if we got JSON data
            if (result.indexOf("{") >= 0 || result.indexOf("[") >= 0) {
                var jsonStart = Math.max(result.indexOf("{"), result.indexOf("["));
                if (jsonStart >= 0) {
                    statusText.text += " (JSON data found)";
                    
                    // Try to extract and format JSON for better readability
                    try {
                        var headersPart = result.substring(0, jsonStart);
                        var jsonPart = result.substring(jsonStart);
                        
                        // If we're showing debug info, keep the original displayResult
                        if (showDebug) {
                            resultsText.text = displayResult + headersPart + "\n\n" + jsonPart;
                        } else {
                            resultsText.text = headersPart + "\n\n" + jsonPart;
                        }
                    } catch (e) {
                        log("Error formatting JSON: " + e.toString());
                    }
                }
            } else {
                statusText.text += " (No JSON data found)";
            }
        } else {
            resultsText.text = "Connection failed: " + conn.error;
            statusText.text = "Connection failed";
        }
    } catch (e) {
        resultsText.text = "Error: " + e.toString();
        statusText.text = "Error";
        log("ERROR: " + e.toString());
    }
};

dialog.show();
