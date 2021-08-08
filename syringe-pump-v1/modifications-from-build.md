# Modification Ideas From Build

After following the build instructions from the OSSPL [1] I realised that:

* Some steps were not descriptive enough
* The Bill of Materials had some wrong quantities
* What 3D printed parts need changes to improve the build process

## List of Modifications

### Carriage (Part #4)

* Modify openSCAD file to print spacing for the 2 linear bearings to fit without having to cut
into either side of the carriage - isn't easy and is also dangerous

* Allow spacing all the way through the 3 rod holes so the builder doesn't have to cut these out
themselves

### Plunger Holder (Part #7)

* Modify this to be wider and taller to fit up to a 60mL syringe - take measurements from 20mL and
60mL syringe plungers so all sizes inclusive will fit

### Body Holders (Part #5)

Currently can think of 2 options for changing this:

* Make an adjustable body holder made for a 60mL syringe, with a fitting for smaller sizes to stop
the syringe moving around

* Modify the openSCAD file to make multiple body holders that can be swapped out once syringe sizes
change

### Extra Points

* Used 4 extra M3 hex nuts for spacing between the motor end and the M3x20mm cap screws holding the
motor in place

* Replaced 2x M3x10mm cap screws with M3x20mm cap screws for attaching the carriage to the plunger holder - 10mm screws were not long enough to hold them together

## References
[1] https://www.appropedia.org/Open-source_syringe_pump#How_to_Build_an_Open-source_Syringe_Pump
