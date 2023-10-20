// JavaScript for subscribing/unsubscribing to topics
function subscribeToTopic() {
    var topic = prompt("Enter the topic you want to subscribe to:");
    var ws = new WebSocket("ws://localhost:8000/subscribe?topic=" + topic);
    // Handle WebSocket connection and message handling here
}

function unsubscribeFromTopic() {
    var topic = prompt("Enter the topic you want to unsubscribe from:");
    var ws = new WebSocket("ws://localhost:8000/unsubscribe?topic=" + topic);
    // Handle WebSocket connection and message handling here
}