# Final Document Planning
---
# Design and Manufacture of a Syringe Pump

## SECTION 1 - BACKGROUND

### Hardware

- 3D Printing
- Electronics
    - Raspberry Pi
        -
    - Motor Driver - A4988
    - NEMA 17 12V 2A Motor
    - Touchscreen
        - Choice of connection: GPIO, Ribbon cable, USB

### Software

- 3D Modelling
- Slicer
- GUI Library

### Medical Hardware

- Commercial Syringe Pumps
- Push for open source hardware (JOGL)
- Current Situation - COVID-19

## INVENTORY

All files I've worked on are included in this GitLab repository, will list below:

### Syringe Pump V1

- STL files (models) of each printed part
- Bill of Materials - all non printed parts and costs
- Datasheets for electronics
- Testing suite (pump_test.py - should separate file into 2 - one for each pump version)
- Build guide (on paper, to be written up in a markdown document)
- Modifications list I wrote to implement for V2

### Syringe Pump V2

- STL files (models) of each printed part
- Testing suite for extra functionality - limit switches to avoid chances of damage
- TODO: Write build guide

### Code
- Testing suite for both pump versions
- Pumpy - Pump operation handler class
- GUI 1 - Kivy version with pump operation code
- GUI 2 - PyQt5 version - better than Kivy, easier design process

### Electronics

- Breadboard version with Elecrow touchscreen
- Breakout board version with USB powered touchscreen (breakout board still failing :/)
- Breadboard with USB powered touchscreen - best alternative currently

## REFERENCES

Science - Pandemic brings mass vaccinations to a halt
Kheiralla et al. - Design and Development of a Low Cost Semi-Automated Poultry Vaccination Machine
Iqbal et al. - Automation of Vaccination and Blood Sampling Procedures
WHO. - Framework for decision-making: implementation of mass vaccination campaigns in the context of COVID-19
Gibson et al. - Vaccinate-assess-move method of mass canine rabies utilising mobile technology data collection in Ranchi, India
Amarante at al. - An Open Source Syringe Pump Controller for Fluid Delivery of Multiple Volumes
Kreiger et al. - Environmental Impacts of Distributed Manufacturing frm 3D Printing of Polymer Components and Products
Wijnen et al. - Open-Source Syringe Pump Library
Booeshaghi et al. - Principles of open source bioinstrumentation applied to the poseidon syringe pump system
Pearce - Quantifying the Value of Open Source Hardware Development
Dryden et al. - Upon the Shoulders of Giants: Open-Source Hardware and Software in Analytical Chemistry
Nature - Make nanotechnology research open-source
Baechler et al. - Distributed Recycling of Waste Polymer into RepRap Feedstock
Garcia et al. - Low-cost touchscreen driven programmable dual syringe pump for life science applications
Pusch et al. - Large volume syringe pump extruder for desktop 3D printers
Pearce et al. - Open-Source Wax RepRap 3D Printer for Rapid Prototyping Paper-Based Microfluidics
