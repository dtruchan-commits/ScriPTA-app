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

// Simple JSON stringify for ExtendScript (since JSON object is not available)
function stringify(obj) {
    if (obj === null) return "null";
    if (obj === undefined) return undefined;
    if (typeof obj === "string") return '"' + obj.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
    if (typeof obj === "number" || typeof obj === "boolean") return obj.toString();
    
    if (obj instanceof Array) {
        var items = [];
        for (var i = 0; i < obj.length; i++) {
            items.push(stringify(obj[i]));
        }
        return "[" + items.join(",") + "]";
    }
    
    if (typeof obj === "object") {
        var pairs = [];
        for (var key in obj) {
            if (obj.hasOwnProperty(key) && obj[key] !== undefined) {
                pairs.push(stringify(key) + ":" + stringify(obj[key]));
            }
        }
        return "{" + pairs.join(",") + "}";
    }
    
    return '""';
}

// Create a basic UI
var dialog = new Window("dialog", "ScriPTA TPM Update Tester");
dialog.orientation = "column";
dialog.alignChildren = ["fill", "top"];
dialog.preferredSize.width = 650;
dialog.preferredSize.height = 700;

// Instructions
var instructionsPanel = dialog.add("panel", undefined, "Instructions");
instructionsPanel.orientation = "column";
instructionsPanel.alignChildren = ["fill", "top"];
instructionsPanel.margins = 10;

var instructionsText = instructionsPanel.add("statictext", undefined, 
    "1. Select endpoint type (UPDATE TPM to test TPM updates)\n" +
    "2. For UPDATE/DELETE/GET by ID: Set TPM ID first\n" + 
    "3. For CREATE/UPDATE: Fill TPM data fields\n" +
    "4. Click Test Connection", 
    {multiline: true}
);
instructionsText.preferredSize.height = 60;

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

// Endpoint selection
var endpointGroup = settingsPanel.add("group");
endpointGroup.add("statictext", undefined, "Endpoint:").preferredSize.width = 80;
var endpointDropdown = endpointGroup.add("dropdownlist", undefined, [
    "GET Layer Config", 
    "GET Swatch Config", 
    "GET TPM Config",
    "GET TPM by ID",
    "CREATE TPM",
    "UPDATE TPM",
    "DELETE TPM"
]);
endpointDropdown.selection = 0;
endpointDropdown.preferredSize.width = 150;

// Path setting (will be auto-generated based on endpoint selection)
var pathGroup = settingsPanel.add("group");
pathGroup.add("statictext", undefined, "Path:").preferredSize.width = 80;
var pathInput = pathGroup.add("edittext", undefined, "/get_layer_config?configName=default");
pathInput.characters = 40;

// TPM-specific input fields
var tpmPanel = settingsPanel.add("panel", undefined, "TPM Data (for CREATE/UPDATE)");
tpmPanel.orientation = "column";
tpmPanel.alignChildren = ["fill", "top"];
tpmPanel.margins = 10;

var tpmIdGroup = tpmPanel.add("group");
tpmIdGroup.add("statictext", undefined, "TPM ID:").preferredSize.width = 80;
var tpmIdInput = tpmIdGroup.add("edittext", undefined, "1");
tpmIdInput.characters = 5;
tpmIdGroup.add("statictext", undefined, "(for UPDATE/DELETE/GET by ID)");

var tpmNameGroup = tpmPanel.add("group");
tpmNameGroup.add("statictext", undefined, "TPM Name:").preferredSize.width = 80;
var tpmNameInput = tpmNameGroup.add("edittext", undefined, "Test TPM");
tpmNameInput.characters = 30;

var tpmDescGroup = tpmPanel.add("group");
tpmDescGroup.add("statictext", undefined, "Description:").preferredSize.width = 80;
var tpmDescInput = tpmDescGroup.add("edittext", undefined, "Test description");
tpmDescInput.characters = 30;

var tpmDimensionsGroup = tpmPanel.add("group");
tpmDimensionsGroup.add("statictext", undefined, "Dimensions:").preferredSize.width = 80;
tpmDimensionsGroup.add("statictext", undefined, "A:");
var tpmAInput = tpmDimensionsGroup.add("edittext", undefined, "100");
tpmAInput.characters = 5;
tpmDimensionsGroup.add("statictext", undefined, "B:");
var tpmBInput = tpmDimensionsGroup.add("edittext", undefined, "200");
tpmBInput.characters = 5;
tpmDimensionsGroup.add("statictext", undefined, "H:");
var tpmHInput = tpmDimensionsGroup.add("edittext", undefined, "50");
tpmHInput.characters = 5;

var tpmVariantGroup = tpmPanel.add("group");
tpmVariantGroup.add("statictext", undefined, "Variant:").preferredSize.width = 80;
var tpmVariantInput = tpmVariantGroup.add("edittext", undefined, "v1.0");
tpmVariantInput.characters = 15;

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

// Endpoint change handler
endpointDropdown.onChange = function() {
    var selection = endpointDropdown.selection.index;
    switch(selection) {
        case 0: // GET Layer Config
            pathInput.text = "/get_layer_config?configName=default";
            break;
        case 1: // GET Swatch Config
            pathInput.text = "/get_swatch_config?colorName=DIELINE";
            break;
        case 2: // GET TPM Config
            pathInput.text = "/get_tpm_config";
            break;
        case 3: // GET TPM by ID
            pathInput.text = "/get_tpm_by_id/" + tpmIdInput.text;
            break;
        case 4: // CREATE TPM
            pathInput.text = "/create_tpm";
            break;
        case 5: // UPDATE TPM
            pathInput.text = "/update_tpm/" + tpmIdInput.text;
            break;
        case 6: // DELETE TPM
            pathInput.text = "/delete_tpm/" + tpmIdInput.text;
            break;
    }
};

// TPM ID change handler (update paths that use ID)
tpmIdInput.onChange = function() {
    var selection = endpointDropdown.selection.index;
    if (selection === 3) { // GET TPM by ID
        pathInput.text = "/get_tpm_by_id/" + tpmIdInput.text;
    } else if (selection === 5) { // UPDATE TPM
        pathInput.text = "/update_tpm/" + tpmIdInput.text;
    } else if (selection === 6) { // DELETE TPM
        pathInput.text = "/delete_tpm/" + tpmIdInput.text;
    }
};


// Function to build TPM JSON payload
function buildTpmPayload() {
    var payload = {
        "TPM": tpmNameInput.text,
        "description": tpmDescInput.text,
        "variant": tpmVariantInput.text
    };
    
    // Add dimensions if they have values
    if (tpmAInput.text && tpmAInput.text !== "") {
        payload.A = parseInt(tpmAInput.text);
    }
    if (tpmBInput.text && tpmBInput.text !== "") {
        payload.B = parseInt(tpmBInput.text);
    }
    if (tpmHInput.text && tpmHInput.text !== "") {
        payload.H = parseInt(tpmHInput.text);
    }
    
    return stringify(payload);
}

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
        var endpointType = endpointDropdown.selection.index;
        
        // Ensure path starts with a slash
        if (path.charAt(0) !== "/") {
            path = "/" + path;
        }
        
        // Determine HTTP method and payload
        var httpMethod = "GET";
        var payload = "";
        
        if (endpointType === 4) { // CREATE TPM
            httpMethod = "POST";
            payload = buildTpmPayload();
        } else if (endpointType === 5) { // UPDATE TPM
            httpMethod = "PUT";
            payload = buildTpmPayload();
        } else if (endpointType === 6) { // DELETE TPM
            httpMethod = "DELETE";
        }
        
        // Log what we're doing
        log("Testing " + httpMethod + " connection to " + host + ":" + port + path);
        if (payload) {
            log("Payload: " + payload);
        }
        
        // Create socket
        var conn = new Socket();
        var result = "";
        
        if (conn.open(host + ":" + port)) {
            // Build request based on format
            var request;
            
            if (format === 0) { // Standard HTTP/1.1
                request = httpMethod + " " + path + " HTTP/1.1\r\n";
                request += "Host: " + host + (port != "80" ? ":" + port : "") + "\r\n";
                request += "User-Agent: InDesign/APIDebugTool\r\n";
                request += "Accept: application/json\r\n";
                
                if (payload) {
                    request += "Content-Type: application/json\r\n";
                    request += "Content-Length: " + payload.length + "\r\n";
                }
                
                request += "Connection: close\r\n\r\n";
                
                if (payload) {
                    request += payload;
                }
            } 
            else if (format === 1) { // Minimal HTTP/1.1
                request = httpMethod + " " + path + " HTTP/1.1\r\n";
                request += "Host: " + host + (port != "80" ? ":" + port : "") + "\r\n";
                
                if (payload) {
                    request += "Content-Type: application/json\r\n";
                    request += "Content-Length: " + payload.length + "\r\n";
                }
                
                request += "\r\n";
                
                if (payload) {
                    request += payload;
                }
            }
            else { // Raw Test - absolute minimum HTTP request
                request = httpMethod + " " + path + " HTTP/1.1\r\nHost: " + host + "\r\n";
                
                if (payload) {
                    request += "Content-Type: application/json\r\n\r\n" + payload;
                } else {
                    request += "\r\n";
                }
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
            
            // Analyze the response
            var operationName = endpointDropdown.selection.text;
            
            // Check for successful HTTP status codes
            if (result.indexOf("HTTP/1.1 200") >= 0) {
                statusText.text = operationName + " - SUCCESS (200 OK)";
            } else if (result.indexOf("HTTP/1.1 201") >= 0) {
                statusText.text = operationName + " - SUCCESS (201 Created)";
            } else if (result.indexOf("HTTP/1.1 204") >= 0) {
                statusText.text = operationName + " - SUCCESS (204 No Content)";
            } else if (result.indexOf("HTTP/1.1 404") >= 0) {
                statusText.text = operationName + " - ERROR (404 Not Found)";
            } else if (result.indexOf("HTTP/1.1 400") >= 0) {
                statusText.text = operationName + " - ERROR (400 Bad Request)";
            } else if (result.indexOf("HTTP/1.1 422") >= 0) {
                statusText.text = operationName + " - ERROR (422 Validation Error)";
            } else if (result.indexOf("HTTP/1.1 500") >= 0) {
                statusText.text = operationName + " - ERROR (500 Server Error)";
            } else {
                statusText.text = "Connection successful";
            }
            
            // Check if we got JSON data
            if (result.indexOf("{") >= 0 || result.indexOf("[") >= 0) {
                var jsonStart = Math.max(result.indexOf("{"), result.indexOf("["));
                if (jsonStart >= 0) {
                    statusText.text += " - JSON response received";
                    
                    // Try to extract and format JSON for better readability
                    try {
                        var headersPart = result.substring(0, jsonStart);
                        var jsonPart = result.substring(jsonStart);
                        
                        // If we're showing debug info, keep the original displayResult
                        if (showDebug) {
                            resultsText.text = displayResult + headersPart + "\n\n--- JSON RESPONSE ---\n" + jsonPart;
                        } else {
                            resultsText.text = headersPart + "\n\n--- JSON RESPONSE ---\n" + jsonPart;
                        }
                    } catch (e) {
                        log("Error formatting JSON: " + e.toString());
                    }
                }
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
