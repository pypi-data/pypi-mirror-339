"""
Read and plot image header times.
"""

import sys

import azcam
import azcam_console.plot
import azcam.fits


def plot_header_times(fileroot="itl.", starting_sequence=1, keyword="UT"):
    """
    Extracts and plots UT time from a sequence of images.
    keyword might be 'UT','TIME-OBS', etc.
    """

    # inputs
    fileroot = azcam.db.parameters.get_local_par(
        "plot_header_times", "fileroot", "prompt", "Enter file root name", fileroot
    )
    starting_sequence = azcam.db.parameters.get_local_par(
        "plot_header_times",
        "starting_sequence",
        "prompt",
        "Enter starting sequence number",
        starting_sequence,
    )
    starting_sequence = int(starting_sequence)
    keyword = keyword.strip("'")  # in case quotes were used

    times = []
    i0 = starting_sequence
    i = i0
    while True:
        img = fileroot + "%.4u" % i
        try:
            ht = azcam.fits.get_keyword(img, keyword)
        except IOError:
            break
        t = ht.split(":")
        tms = float(t[2]) + 60.0 * float(t[1]) + 3600.0 * float(t[0])
        if i == i0:
            tms0 = tms
        delta = tms - tms0
        print("Image %3d, UT %s, Time: %.3f" % (i, ht, delta))
        times.append(delta)
        i = i + 1

    # plot
    fig, ax = azcam_console.plot.plt.subplots(constrained_layout=True)
    fignum = fig.number
    azcam_console.plot.move_window(fignum)
    azcam_console.plot.plt.title("%s in Header" % keyword)
    azcam_console.plot.plt.xlabel("Image Number")
    azcam_console.plot.plt.ylabel("Relative Time (sec)")
    ax.grid(1)
    azcam_console.plot.plt.plot(times)
    azcam_console.plot.save_figure(fignum, "%s_relative.png" % keyword)

    # make differences
    for j in range(0, len(times) - 1):
        times[j] = times[j + 1] - times[j]
    times = times[:-1]
    fig, ax = azcam_console.plot.plt.subplots(constrained_layout=True)
    fignum = fig.number
    azcam_console.plot.move_window(fignum)
    azcam_console.plot.plt.title("%s Difference" % keyword)
    azcam_console.plot.plt.xlabel("Image Number")
    azcam_console.plot.plt.ylabel("Relative Time (sec)")
    ax.grid(1)
    azcam_console.plot.plt.plot(times)
    azcam_console.plot.update()
    azcam_console.plot.save_figure(fignum, "%s_difference.png" % keyword)

    azcam_console.plot.plt.show()

    return


if __name__ == "__main__":
    args = sys.argv[1:]
    plot_header_times(*args)
