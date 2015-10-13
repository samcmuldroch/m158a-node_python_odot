/// Examples from https://www.npmjs.com/package/osc --- please see that page for more information

/// variables:
var osc = require('osc'),
    udpPort = new osc.UDPPort({
        localAddress: "0.0.0.0",    // "128.0.0.1" works for localhost, also
        localPort: 54344            // this will be the port in the "udpsend" in Max -- port Max SENDS TO.
    });

/// open the port:
udpPort.open();

/// Send a bundle:
udpPort.send({
    timeTag: osc.timeTag(0),    // this is required, don't question it
    packets: [
    // an odot bundle in javascript is just a JSON with "address" and "args" (can contain a list):
        {
            address: "/frequency",
            args: 440
        },
        {
            address: "/envelope/line",
            args: [1.0, 20, 0.0, 1000]
        }
    ]
    /*
        The resulting bundle for the above would be:
            /frequency : 440,
            /envelope/line : [1., 20, 0., 1000]
        -- see the o.display in the example Max patch
    */
}, "127.0.0.1", 54345);     // note this port here -- this is the port NODE sends to -- udpreceive in Max

/// Receive an OSC Bundle (in case you need to send data to your Node server):
udpPort.on("bundle", function (oscBundle) {
    console.log("An OSC bundle just arrived!", oscBundle); /// to see the bundle that arrived

    /// to get addresses / values:
    for (p in oscBundle.packets) {
        console.log(oscBundle.packets[p].address);
        console.log(oscBundle.packets[p].args);
    }
    /// trigger the sound in any case:
    go();
});

/// function to trigger every time something is sent (just as the example above:)
var go = function() {
    udpPort.send({
    timeTag: osc.timeTag(0),
    packets: [
        {
            address: "/frequency",
            args: 440
        },
        {
            address: "/envelope/line",
            args: [1.0, 20, 0.0, 1000.0]
        }
    ]
    }, "127.0.0.1", 54345);
};
