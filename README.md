
# Alexa-Device-Management

This repository contains a Python script for managing devices connected to the Amazon Alexa API. The script provides functionality to retrieve and delete entities related to an Amazon Alexa skill.

⚠️⚠️ **Warning:** This script is not intended to be used for malicious purposes. I am not responsible for any damage caused by the use of this script. Use at your own risk. Also note that this script is not officially supported by Amazon and may break at any time. It is also not recommended to use this script for a small number of devices, as it takes a while to set up. If you only want to delete a few devices, it is probably faster to do it manually. ⚠️⚠️

# Prerequisites

The script is written in Python 3.11 and requires the following packages:
- requests
_see requirements.txt for more details_ 
Run `pip install -r requirements.txt` to install required packages

To get the needed HTTP headers and cookie information, you will need to download some kind of http traffic sniffer.  
I used [HTTP Catcher](https://apps.apple.com/de/app/http-catcher/id1445874902), which is only available for iOS.  
Tools like [HTTP Toolkit](https://httptoolkit.tech/) should for android based devices, but this app requires a rooted device.  
_Note: For using an HTTP Sniffer on android, you will need to install the certificate of the sniffer app on your device. Proxy based sniffers will not work, as the Alexa app (and most other ones like Google and PayPal) uses certificate pinning._

You also need to have a valid Amazon account and access to the account you want to delete entities from.

# Usage

1. Download and install a HTTP Sniffer on your device
2. Open the Alexa app and log in with the account you want to delete entities from
3. Navigate to the `Devices` tab
4. Open the HTTP Sniffer and start a new capture
5. In the Alexa app, refresh the device list by pulling down
6. Let the page load completely
7. Stop the capture in the HTTP Sniffer
8. Search for the `GET /api/behavioral/entities` request in the HTTP Sniffer
9. Copy the value of the `Cookie` header and paste it into the `GET_COOKIE` variable in the script (Most likely, you will find the cookie value to be very long.)
10. Copy the value of the `x-amzn-RequestId` header and paste it into the `GET_X_AMZN_REQUESTID` variable in the script
11. Copy the value of the `x-amzn-alexa-app` header and paste it into the `GET_X_AMZN_ALEXA_APP` variable in the script  
    **_11.1._** (only do if you want to try and speed up the process). You can now try to use the same cookie for both getting and deleting entities. If you want to do that leave the `CSRF` variable empty and skip to step 13
12. Go back to the Alexa app and click on one of the devices you want to delete and go to the `Device Settings` page
13. Open the HTTP Sniffer and start a new capture
14. In the Alexa app, click on the `Delete Device` button
15. Go back to the HTTP Sniffer and stop the capture
16. Search for the `DELETE /api/phoenix/appliance` request in the HTTP Sniffer
17. Copy the `DELETE_COOKIE`, `DELETE_X_AMZN_REQUESTID`, `DELETE_X_AMZN_ALEXA_APP` and past them like you did in step 9-11.  
    **_17.1._** If you skipped step 11.1, you will need to copy the value of the `csrf` parameter in the request body and paste it into the `CSRF` variable in the script
18. You can now try and run the script. If it works, you should see a list of all devices connected to the account you are logged in with. If you get an error, see the [Troubleshooting](/#troubleshooting) section for more information.

# Troubleshooting

1. Try and change the `HOST` address in the script to your local amazon address. You can find it in the HTTP Sniffer in both the requests you copied the headers from.
2. Try and change the `USER_AGENT` variable in the script to the one you find in the HTTP Sniffer in both the requests you copied the headers from.
3. If you used step 11.1 try and change the `CSRF` variable in the script to the one you find in the HTTP Sniffer in the `DELETE` request.
4. If you used the script some time ago, try and update the `GET_COOKIE` variable in the script to the one you find in the HTTP Sniffer in the `GET` and/or `DELETE` request.

# Inspiration

An amazon employee told me "have fun with that" when I asked him how to delete devices connected to an Alexa skill. So I did.

# Inscription

Thanks to @[HennieLP](https://github.com/hennielp) for helping me with the script and the README (also thanks to him I didn't have to root my phone to get a HTTP Sniffer running <3)
