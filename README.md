# Design and Manufacture of a Syringe Pump

Research into Free Open Source Hardware (FOSH) has been extremely useful for academics and hobbyists alike. One such area includes the use of a basic linear actuator to create a rudimentary syringe pump. This has its uses in medical operations (palliative care/hospices/chemotherapy), chemical engineering (reactionware, chemical synthesis) and mechanical operation (life science, nanotechnology).

---
## Table of Contents

1. [Syringe Pump v1](./syringe-pump-v1/README.md)
   1. [Build Guide](./syringe-pump-v1/build-guide.md)
   2. [Modifications](./syringe-pump-v1/modifications-from-build.md)
2. [Syringe Pump v2](./syringe-pump-v2/README.md)
   1. [Build Guide](./syringe-pump-v2/build-guide.md)
3. [Electronics](./electronics/README.md)
4. [Testing Suite](./testing-suite/README.md)
   1. [Pump Operation Calculations](./testing-suite/pump-maths.md)
5. [Pump UI](./pump-ui/README.md)
   1. [Kivy GUI](./pump-ui/kivy-design/README.md)
   2. [PyQt GUI](./pump-ui/qt-design/README.md)
6. [Android Application](./android-app/README.md)
   1. [Pumpy App](./android-app/Pumpy/README.md)
   2. [Bluetooth Handler](./bluetooth-handler/README.md)

---
## Project Objectives

My main objective is to build a version of the Open Source Syringe Pump [1], adding several improvements from other projects that build upon it including:

* Upgraded Carriage for simpler bearing insertion and adjustable syringe holders
* Open syringe clamp for easy removal
* Limit switches for automatic position detection
* Ability to withdraw liquid automatically without removing the syringe
* Touchscreen interface using Python and PyQt 5 for basic user-friendly operation
* Android application to interact with the Syringe Pump via Bluetooth

I also plan to discuss the use of Free and Open Source hardware, the history behind medical syringe pumps and
the process by which we can build and program one with a touchscreen interface and Android remote operation for £150.

Overall I hope to show the process of utilising open source hardware and software to build and manufacture a product that rivals current consumer level technology, alongside providing a deliverable that could be put together and operated by a layman.

---
## What are Syringe Pumps?
Syringe Pumps (or Syringe Drivers) are battery powered pumps used to deliver medication into the body at a constant
rate. Patients are usually given them for a number of reasons:

* Nausea or Vomiting
* Difficulty swallowing oral medicine
* To avoid staff giving injected medicines frequently
* Unable to absorb medicines through their gut effectively

They are commonly used with patients receiving end-of-life care but are useful for managing the above symptoms
during any stage of care.

## Building a Pump

There exist many forms of the Open Source Syringe Pump that have been designed and released online. Having researched a number of these I decided upon 2 designs to work with and implement my modifications to. The STL files for 3D printing, BOM (Bill of Materials) and build guides are located in:

* syringe-pump-v1
  - Based on the Open Source Syringe Pump Library
  - Overhauls the electronics from the original design
  - Adds modifications to improve usability

* syringe-pump-v2
  - Upgrades to the Syringe Pump v1
  - Incorporates design elements from Andrey Samokhins design from Thingiverse
  - Larger side supports

The software to utilise each of these is still in development in the pump-ui and stepper-driver-code folders, but will
be combined into one piece of software with settings for both styles of pump.
