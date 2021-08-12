# Validate project 

## Description

The script runs algorithm which chooses the best model from generated data. The algorithm work principle is the following
  * find the filename and its coresponding IOU value
  * compare with other projects generated results
  * if the values differences are smaller than chop_percentage(given by me), then ignore them, otherwise keep them
  * in the end, get the arithmetic average and based on them decide the best project

### Dependencies

 * windows 
  


### Executing program

```
python3 validate_realise.py -d "input directory" or -f "input files" -o "output file"
