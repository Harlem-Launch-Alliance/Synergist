# Catalyst-UI
A graphical interface for sounding rocket telemetry

## Quickstart
1. Install Python 3 and relevant libraries
1. Clone this repository
1. Run `python src/main.py`
1. Specify the port for your receiver
1. Open your browser on `localhost:8050`

## Specifications
This graphical user interface will work with any flight computer that transmits in the following format:

- All transmitted data must be a string representation of an array
- Elements should be separated by spaces
- The first element should be a datatype identifier

Identifiers:
| Identifier | Value 1 | Value 2 | Value 3 | Sample String |
|---------|--------|--------|--------|--------|
| 0 | int flightState* (0-3) ||| "0 2"|
| 1 | float altitude(m) ||| "1 435.78"|
| 2 | float attitude.x(deg) | float attitude.y(deg) | float attitude.z(deg) | "2 20.5 8.1 175.4" |
| 3 | float GPS.lat | float GPS.long || "3 75.1234 43.9876" |

Note: flight states of 0-3 map to "On Pad", "Ascending", "Descending", "Landed" respectively.