# threadPortraitAlgorithm
Making portraits from thread

This algorithm takes as input an image you want to draw, and will output:
- a series of numbers corresponding to each nail where the thread should be placed (stored in results.txt), and 
- [optional] simulated images of what the result will look like after x iterations

To run the script, call `py main.py [args]` from the command line with the following arguments: 
- `BOARD_WIDTH`: width of the board in centimeters
- `PIXEL_WIDTH`: suggest keeping this constant and changing board width only
- `LINE_TRANSPARENCY`: how many lines overlapped required to reach black (value between 0 to 1)
- `NUM_NAILS`: how many nails to place on the board
- `MAX_ITERATIONS`: how many thread segments to place before algorithm terminates
- `BEAUTIFY`: determine beautifying the output path, result path and process or not