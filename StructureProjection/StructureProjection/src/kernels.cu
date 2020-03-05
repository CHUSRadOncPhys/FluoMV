#include "cuda_runtime.h"
#include <stdlib.h>
#include<stdio.h>
#include<kernels.h>

//using namespace std;
//************************************************************************************************************************
//************************************************************************************************************************
__global__ void ProjectionGPU(float *d_Label, int *d_im_EPID, float *d_sourcePoint,  float *d_resolution, float d_BeamAngle, int NbRows, int NbCols, int NbSlices, int d_PanelNbPixels, float d_PixDimEPID, float d_TableAngle, int Xmin,int Xmax,int Ymin,int Ymax,int Zmin,int Zmax,float offsetX_dicom,float offsetY_dicom,float offsetZ_dicom)
{
	
    int x_target = blockIdx.x;
    int y_target = threadIdx.x;

	if (x_target<d_PanelNbPixels && y_target<d_PanelNbPixels){

		
    float ai,aj;
    float targetpoint0, targetpoint1,targetpoint2;
    float axy,bxy,axz,bxz,ayx,ayz,byx,byz,azx,azy,bzx,bzy;
    float x_mm,y_mm,z_mm;
    int y_intersectX,z_intersectX,x_intersectY,z_intersectY,x_intersectZ,y_intersectZ;
    int xL,yL,zL;
        
    ai = (x_target-d_PanelNbPixels/2+0.5)*d_PixDimEPID;
    aj = (y_target-d_PanelNbPixels/2+0.5)*d_PixDimEPID;
        
    float PI = 3.14159;
        
    targetpoint0 = cos(d_BeamAngle*PI/180)*ai-sin(d_BeamAngle*PI/180)*600;
    targetpoint1 = sin(d_BeamAngle*PI/180)*ai+cos(d_BeamAngle*PI/180)*600;
    targetpoint2 = aj;
        
    axy = (targetpoint1-d_sourcePoint[1])/(targetpoint0-d_sourcePoint[0]);
    bxy = d_sourcePoint[1]-axy*d_sourcePoint[0];
    axz = (targetpoint2-d_sourcePoint[2])/(targetpoint0-d_sourcePoint[0]);
    bxz = d_sourcePoint[2]-axz*d_sourcePoint[0];

    for(int x=Xmin-1;x<(Xmax+2);x++){
        x_mm = x*d_resolution[0] - offsetX_dicom;
        y_intersectX = (int)round(((x_mm*axy+bxy)+offsetY_dicom)/d_resolution[1]);
        z_intersectX = (int)round(((x_mm*axz+bxz)+offsetZ_dicom)/d_resolution[2]);
        xL=x;

                
        if ((xL >= 0) and (xL < NbRows) and (y_intersectX >= 0) and (y_intersectX < NbCols) and (z_intersectX >= 0) and (z_intersectX < NbSlices)){
                    
            if(d_Label[z_intersectX*NbRows*NbCols+y_intersectX*NbCols+xL]>0){
                d_im_EPID[x_target*d_PanelNbPixels+y_target] = 1;
                x = Xmax+1;
            }
        }
    }
    
    if(d_im_EPID[x_target*d_PanelNbPixels+y_target] ==0){
        ayx = (targetpoint0-d_sourcePoint[0])/(targetpoint1-d_sourcePoint[1]);
        byx = d_sourcePoint[0]-ayx*d_sourcePoint[1];
        ayz = (targetpoint2-d_sourcePoint[2])/(targetpoint1-d_sourcePoint[1]);
        byz = d_sourcePoint[2]-ayz*d_sourcePoint[1];
                
                
        for(int y=Ymin-1;y<(Ymax+2);y++){
            y_mm = y*d_resolution[1] - offsetY_dicom;
            x_intersectY = (int)round(((y_mm*ayx+byx)+offsetX_dicom)/d_resolution[0]);
            z_intersectY = (int)round(((y_mm*ayz+byz)+offsetZ_dicom)/d_resolution[2]);
            yL=y;
                    
            if ((yL >= 0) and (yL < NbCols) and (x_intersectY >= 0) and (x_intersectY < NbRows) and (z_intersectY >= 0) and (z_intersectY < NbSlices)){
                        
                if(d_Label[z_intersectY*NbRows*NbCols+yL*NbCols+x_intersectY]>0){
                    d_im_EPID[x_target*d_PanelNbPixels+y_target] = 1;
                    y = Ymax+1;
                }
            }
        }
    }
    
    if(d_im_EPID[x_target*d_PanelNbPixels+y_target] ==0){
        azx = (targetpoint0-d_sourcePoint[0])/(targetpoint2-d_sourcePoint[2]);
        bzx = d_sourcePoint[0]-azx*d_sourcePoint[2];
        azy = (targetpoint1-d_sourcePoint[1])/(targetpoint2-d_sourcePoint[2]);
        bzy = d_sourcePoint[1]-azy*d_sourcePoint[2];
               
        for(int z=Zmin-1;z<(Zmax+2);z++){
            z_mm = z*d_resolution[2] - offsetZ_dicom;
            x_intersectZ = (int)round(((z_mm*azx+bzx)+offsetX_dicom)/d_resolution[0]);
            y_intersectZ = (int)round(((z_mm*azy+bzy)+offsetY_dicom)/d_resolution[1]);
            zL=z;
                    
            if ((y_intersectZ >= 0) and (y_intersectZ < NbCols) and (x_intersectZ >= 0) and (x_intersectZ < NbRows) and (zL >= 0) and (zL < NbSlices)){
                        
                if(d_Label[zL*NbRows*NbCols+y_intersectZ*NbCols+x_intersectZ]>0){
                    d_im_EPID[x_target*d_PanelNbPixels+y_target] = 1;
                    z = Zmax+1;
                }
            }
        }
    }
        
        
    }

}
