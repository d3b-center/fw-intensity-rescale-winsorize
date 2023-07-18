# SDK gear to rescale and winorize images

This gear takes the input file and:
1. makes signal intensities outside of 1st/99th percentile to be equal to the value of the 1st/99th percentile ("winorize")
2.  rescales all intensity values to be within 0-255 range
3.  converts all values to integer data type
4.  save normalized image to same acquisition container as the input file

## Usage

Run at the file-level (either in batch or on a single session).

### Inputs

input_file: image to be processed (nifti)

### Configuration

* __debug__ (boolean, default False): Include debug statements in output.

### Limitations

Current limitations of the gear are as follows:

* doesn't run in batch mode