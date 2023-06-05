# Package Delivery Optimization System

This project was developed as part of a university course to showcase the application of algorithms and data structures in solving a real-world problem. The goal of the project was to create an efficient delivery route and distribution system for a hypothetical client called Western Governors University Parcel Service (WGUPS). The project implements various algorithms and data structures to optimize the delivery process and ensure timely delivery of packages.
NOTE:  The use of the Python dictionary data structure was not permitted.  Instead, a hash function was implemented and used in its place.

The requirements are as follows:
- The total mileage for all trucks by the end of the day is 140.
- Each truck can carry at most 16 packages.
- The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
- There are no collisions.
- Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
- Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
- The delivery and loading times are instantaneous, i.e., no time passes while at a delivery or when moving packages to a truck at the hub (that time is factored into the calculation of the average speed of the trucks).
- There is up to one special note associated with a package.
- The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S State St., Salt Lake City, UT 84111) until 10:20 a.m.
- The distances provided in the WGUPS Distance Table are equal regardless of the direction traveled.
- The day ends when all 40 packages have been delivered.

## Technologies Used
- Programming Language: Python 3.10.5
- Libraries: (No 3rd party libraries permitted)
- Development Environment: PyCharm 2022.1.4 (Community Edition)

## Usage
1. Run the main script: 'python main.py'
2. Follow on-screen prompts to start the simulation. User has the choice to view all packages or a specific package at any given time.
