import pytest
import DataIntegration_Averages as dia
import ReadResult_Content as rrc

#tests ability of the findAverage function
def test_one():
    
    inputPath = "./Input_Data/"
    outputPath = "./Output_Data/"
    testPass = dia.findAverages(inputPath, outputPath)
    assert testPass == 1

#tests ability to print output values
def test_two():
    
    testPass = rrc.PrintResults()
    assert testPass == 1
    