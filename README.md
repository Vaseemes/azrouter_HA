[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W1JVAKW)
<br>
# AZrouter_HA<br>
Two very basic Python scripts that are reading values from AZrouter device and are adding them to HomeAssistant.<br>
<br>
**!!! THESE SCRIPTS ARE NOT RUNNING IN THE HOMEASSISTANT. YOU CAN START THEM UP ON SEPARATE WINDOWS MACHINE/SERVER AND LEAVE THEM RUNNING !!!**<br>

## **Requirements**<br>
Python installed<br>
Python Playwright package installed<br>
Samba Share addon in Home Assistant running<br>

## **Goal/Scope**<br>
Reading values from AZrouter SMART<br>
- Consumption/production from/to grid<br>
- Power to boiler<br>
- Boiler temperature<br>

## Installation

Install latest Python<br>
After installing Python, open command line and write:
```
py -m pip install playwright
```
<br>
You can then close the command line.<br>
Next in HA install Samba Share addon and set it up (username, password)<br>

### Now we need to add files to HA<br>
You can put these files in whatever folder in the HA installation you want, but if you do, you need to define that path in the .pyw files.<br>
Access your HA via Windows (Samba share) and in folder "/config/www/" create three empty files:<br>
azrouter.txt<br>
azrouter_bojler_nahrivani.txt<br>
azrouter_bojler.txt<br>
<br>
Download and open the .pyw files from this repository. Open the "combined azrouter.pyw" in notepad or IDE of your choice.
<br>
Here you need to change these:<br>
```
username = "YOUR-USERNAME"
password = "YOUR-PASSWORD"
```
Replace "YOUR-USERNAME" and "YOUR-PASSWORD" with the azrouter.local login details.<br>
In this file you also need to change IP of your HomeAssistant here:<br>

```
output_file_path = "//YOUR-HA-IP_ADDRESS/config/www/azrouter.txt"
output_file_path2 = "//YOUR-HA-IP_ADDRESS/config/www/azrouter_bojler_nahrivani.txt"
```
<br>

Do the same for the "azrouter_bojler.pyw" file.<br>

### Now we need add to these values to HA<br>
Open configuration.yaml and add these:<br>

```
sensor:

  - platform: file
    name: WHATEVER NAME YOU WANT
    file_path: /config/www/azrouter.txt
    unit_of_measurement: "W"
    scan_interval: 5

  - platform: file
    name: WHATEVER NAME YOU WANT
    file_path: /config/www/azrouter_bojler.txt
    unit_of_measurement: "°C"
    scan_interval: 120

  - platform: file
    name: WHATEVER NAME YOU WANT
    file_path: /config/www/azrouter_bojler_nahrivani.txt
    unit_of_measurement: "W"
    scan_interval: 5
    
```

The boiler temperature reading and power that is going to the boiler are now ready to use in HA.<br>
But if you want to measure consumption/production from/to the grid you also need to create template sensors and helpers. Here is the idea of the code for template sensors you can use:

```
template:

  - sensor:
      - name: "Consumption times minus 1"
        unit_of_measurement: "W"
        state_class: measurement
        device_class: power
        unique_id: "sensor.consumption_times_minus_one"
        state: >
          {% set power = (states('sensor.consumption') | float)*-1 %}
          {{ 0 if power < 0 else power }}

  - sensor:
      - name: "Export electricity"
        unit_of_measurement: "W"
        state_class: measurement
        device_class: power
        unique_id: "senzor.export_electricity"
        state: >
          {% set power = (states('sensor.consumption') | float)%}
          {{ 0 if power < 0 else power }}
```

AZ Router returns both plus and minus values. That's why we need to use times -1 in the first sensor and values only higher than 0. This is the consumption from the grid.<br>

The second sensor gives us value of the power export.<br>

If you want to use these sensors in the Energy card or elsewhere to measure Energy in Wh, kWh you need to create helper Riemann sum integral (https://www.home-assistant.io/integrations/integration/) Setup is pretty straightforward, so I won't go into the detail.<br>


## Examples/Use case<br>
### Power Flow Card Plus<br> 
https://github.com/flixlix/power-flow-card-plus
<br> 

<br>

![My Remote Image](https://github.com/Vaseemes/azrouter_HA/blob/main/power_flow_card_plus.jpg?raw=true)
<br>


### Energy Card<br>

<br>

![My Remote Image](https://github.com/Vaseemes/azrouter_HA/blob/main/energy_card.jpg?raw=true)



