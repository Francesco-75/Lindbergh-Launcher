import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# Function to save configuration and launch the application
def save_and_launch():
    config = gather_config()
    if not config:
        return

    # Save configuration to lindbergh.conf
    if not save_to_file("lindbergh.conf", config):
        return

    # Launch lindbergh.elf
    try:
        subprocess.Popen(["./lindbergh.elf"])
        messagebox.showinfo("Success", "Lindbergh launched successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "The file 'lindbergh.elf' was not found in the current directory.")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied when trying to execute 'lindbergh.elf'.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch Lindbergh: {e}")

# Function to save configuration only
def save_configuration():
    config = gather_config()
    if not config:
        return

    # Save configuration to lindbergh.conf
    if save_to_file("lindbergh.conf", config):
        messagebox.showinfo("Success", "Configuration saved successfully!")

# Function to execute a command and display the result
def show_serial_ports():
    try:
        subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", "sudo dmesg | grep tty; exec bash"])
    except FileNotFoundError:
        messagebox.showerror("Error", "No terminal emulator found to execute the command.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open terminal: {e}")

# Gather configuration from the UI
def gather_config():
    try:
        config = (
            f"WIDTH {resolution_var.get().split('x')[0]}\n"
            f"HEIGHT {resolution_var.get().split('x')[1]}\n"
            f"FULLSCREEN {fullscreen_var.get()}\n"
            f"INPUT_MODE {input_mode_var.get().split(' - ')[0]}\n"
            f"NO_SDL {no_sdl_var.get().split(' - ')[0]}\n"
            f"REGION {region_var.get()}\n"
            f"FREEPLAY {freeplay_var.get()}\n"
            f"EMULATE_JVS {emulate_jvs_var.get()}\n"
            f"EMULATE_RIDEBOARD {emulate_rideboard_var.get()}\n"
            f"EMULATE_DRIVEBOARD {emulate_driveboard_var.get()}\n"
            f"EMULATE_MOTIONBOARD {emulate_motionboard_var.get()}\n"
            f"JVS_PATH {jvs_path_var.get()}\n"
            f"SERIAL_1_PATH {serial_1_path_var.get()}\n"
            f"SERIAL_2_PATH {serial_2_path_var.get()}\n"
            f"GPU_VENDOR {gpu_vendor_var.get().split(' - ')[0]}\n"
            f"DEBUG_MSGS {debug_msgs_var.get()}\n"
            f"HUMMER_FLICKER_FIX {hummer_flicker_fix_var.get()}\n"
            f"KEEP_ASPECT_RATIO {keep_aspect_ratio_var.get().split(' - ')[0]}\n"
            f"OUTRUN_LENS_GLARE_ENABLED {outrun_lens_glare_enabled_var.get().split(' - ')[0]}\n"
            f"FPS_LIMITER_ENABLED {fps_limiter_var.get().split(' - ')[0]}\n"
            f"FPS_TARGET 60\n"
            f"LGJ_RENDER_WITH_MESA {lgj_render_with_mesa_var.get().split(' - ')[0]}\n"
            f"PRIMEVAL_HUNT_MODE {primeval_hunt_mode_var.get().split(' - ')[0]}\n"
            f"LINDBERGH_COLOUR {lindbergh_colour_var.get()}\n"
            f"SRAM_PATH sram.bin\nEEPROM_PATH eeprom.bin\n"
        )
        return config
    except Exception as e:
        messagebox.showerror("Error", f"Failed to gather configuration: {e}")
        return None

# Save the configuration string to a file
def save_to_file(filename, content):
    try:
        with open(filename, "w") as conf_file:
            conf_file.write(content)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write configuration file: {e}")
        return False

# Create the main window
root = tk.Tk()
root.title("Lindbergh Launcher")

# Create a frame for the resolution options
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add UI elements for each configuration option
config_options = [
    ("Select Resolution:", resolutions := ["640x480", "800x600", "1024x768", "1280x1024", "800x480", "1024x600", "1280x768", "1360x768", "1920x1080"], resolutions[0]),
    ("Fullscreen Mode:", ["0", "1"], "0"),
    ("Input Mode:", ["0 - SDL/X11 and EVDEV inputs", "1 - SDL/X11 inputs only", "2 - EVDEV raw inputs only"], "0 - SDL/X11 and EVDEV inputs"),
    ("NO_SDL:", ["0", "1 - Fixes SRTV boost bar"], "0"),
    ("REGION:", ["EX", "JP", "US"], "EX"),
    ("FREEPLAY:", ["0", "1"], "0"),
    ("EMULATE_JVS:", ["0", "1"], "0"),
    ("EMULATE_RIDEBOARD:", ["0", "1"], "0"),
    ("EMULATE_DRIVEBOARD:", ["0", "1"], "0"),
    ("EMULATE_MOTIONBOARD:", ["0", "1"], "0"),
    ("JVS_PATH:", ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"], "/dev/ttyUSB0"),
    ("SERIAL_1_PATH:", ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"], "/dev/ttyUSB0"),
    ("SERIAL_2_PATH:", ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"], "/dev/ttyUSB0"),
    ("GPU_VENDOR:", ["0 - Autodetect", "1 - NVidia", "2 - AMD", "3 - ATI(AMD-PRO)", "4 - Intel", "5 - Unknown"], "0 - Autodetect"),
    ("DEBUG_MSGS:", ["0", "1"], "0"),
    ("HUMMER_FLICKER_FIX:", ["0", "1"], "0"),
    ("KEEP_ASPECT_RATIO:", ["0", "1 - Keep aspect ratio (4:3) in games"], "0"),
    ("OUTRUN_LENS_GLARE_ENABLED:", ["0 - Disable Glare effect in OutRun", "1"], "0 - Disable Glare effect in OutRun"),
    ("FPS_LIMITER_ENABLED:", ["0", "1 - if you want to limit the FPS in games that are not limited like OutRun2"], "0"),
    ("LGJ_RENDER_WITH_MESA:", ["0", "1 - if you want to render LGJ using the mesa patches instead of nVidia (fixes some glitches)"], "0"),
    ("PRIMEVAL_HUNT_MODE:", [
        "0 - Leaves everything as default",
        "1 - No touch screen (Default mode)",
        "2 - Side by Side",
        "3 - 3ds mode 1 (Touch screen to the right)",
        "4 - 3ds mode 2 (Touch screen to the bottom)"
    ], "0 - Leaves everything as default"),
    ("LINDBERGH_COLOUR:", ["YELLOW", "RED"], "YELLOW")
]

variables = []
for i, (label_text, options, default) in enumerate(config_options):
    ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5)
    var = tk.StringVar(value=default)
    ttk.Combobox(frame, textvariable=var, values=options, state="readonly", width=60).grid(row=i, column=1, padx=5, pady=5)
    variables.append(var)

# Assign variables for each configuration
(
    resolution_var, fullscreen_var, input_mode_var, no_sdl_var, region_var, freeplay_var,
    emulate_jvs_var, emulate_rideboard_var, emulate_driveboard_var, emulate_motionboard_var,
    jvs_path_var, serial_1_path_var, serial_2_path_var, gpu_vendor_var, debug_msgs_var,
    hummer_flicker_fix_var, keep_aspect_ratio_var, outrun_lens_glare_enabled_var, fps_limiter_var,
    lgj_render_with_mesa_var, primeval_hunt_mode_var, lindbergh_colour_var
) = variables

# Add Save Configuration button
ttk.Button(root, text="Save Configuration", command=save_configuration).grid(row=i + 1, column=0, pady=10, padx=10, sticky=(tk.W, tk.E))
# Add Save and Launch button
ttk.Button(root, text="Save and Launch", command=save_and_launch).grid(row=i + 2, column=0, pady=10, padx=10, sticky=(tk.W, tk.E))

# Add button to check serial ports
ttk.Button(root, text="which /dev/ttyS* is my serial port?", command=show_serial_ports).grid(row=i + 3, column=0, pady=10, padx=10, sticky=(tk.W, tk.E))

# Main loop
root.mainloop()

