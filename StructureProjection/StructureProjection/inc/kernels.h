#ifndef kernels_H
#define kernels_H

#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <stdio.h>

//*****************************************************************************************************************

//using namespace std;
__global__ void ProjectionGPU(float *d_Label, int *d_im_EPID, float *d_sourcePoint,  float *d_resolution, float d_BeamAngle, int NbRows, int NbCols, int NbSlices, int d_PanelNbPixels, float d_PixDimEPID, float d_TableAngle, int Xmin,int Xmax,int Ymin,int Ymax,int Zmin,int Zmax,float offsetX_dicom,float offsetY_dicom,float offsetZ_dicom);

#endif 