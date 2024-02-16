# Wavy
## Overview

This audio measurement application is designed to record audio from a selected input device, perform FFT (Fast Fourier Transform) analysis, and display the results through an interactive GUI. It allows for multiple measurements, overlaying plots for comparison, and dynamic interaction with the plotted data.

## Features

- **Audio Recording**: Captures audio using the default or selected microphone device.
- **FFT Analysis**: Computes the Fast Fourier Transform of the recorded audio to analyze the frequency spectrum.
- **Interactive Plotting**: Visualizes the frequency spectrum with the ability to zoom, pan, and toggle the visibility of individual measurements.


## Installation

To run this application, you will need Python 3.x installed on your system. The application depends on several external libraries, which can be installed via pip:


## Usage

1. **Starting the Application**: Run the main script from your terminal or command prompt:

    ```
    python Wavy00.py
    ```
2. To add new Audio processing features, you can add them in the following file

    ```
    python Measurement00.py
    ```

4. **Recording Audio**: Click the "Start Measurement" button to begin recording audio. Each recording is automatically stored and listed in the treeview as a new measurement (e.g., Measurement 1, Measurement 2, etc.).

5. **Viewing FFT Analysis**: After a measurement is recorded, its FFT analysis is immediately plotted. You can toggle the visibility of each measurement's plot by checking or unchecking its corresponding checkbox in the treeview.

6. **Interacting with Plots**: Use the toolbar above the plot to zoom in, pan, or reset the plot view. This allows for detailed examination of specific frequency components.

## Appearance
![AppScreenshot_SpeakerMeasurement](https://github.com/SrikarWritesCode/Wavy/Images/AppScreenshot_SpeakerMeasurement.png)


## Customization

The application's appearance and functionality can be customized by modifying the `GUIController.py` and `MeasurementController.py` scripts. This includes changing the audio recording parameters, adjusting the FFT computation, or enhancing the GUI layout and interactivity.

## Known Issues

- The appearance of the Matplotlib toolbar is determined by Tkinter's default styling, which may appear outdated on some systems.
- The application does not currently support selecting different audio input devices from the GUI.
- I plan to implement multi-input interfaces, and also near fied measurements. 

## Contributing

Contributions to improve the application are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-source.
