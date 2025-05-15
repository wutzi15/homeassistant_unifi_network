# Unifi Custom Integration
An integration for Home Assistant read network information from Unifi devices.


## Installation

1. Copy the `unifi_custom` folder into your Home Assistant custom components directory.
2. Restart Home Assistant.
3. Add the Integration via the Home Assistant UI.
4. Configure with your Unifi controller IP address and API key (see below).

## Obtaining API Key
1. Open your Site in UniFi Site Manager at unifi.ui.com.
2. Click on Control Plane -> Admins & Users.
3. Select your Admin.
4. Click Create API Key.
5. Add a name for your API Key.
6. Copy the key and store it securely, as it will only be displayed once.
7. Click Done to ensure the key is hashed and securely stored.
8. Use the API Key.