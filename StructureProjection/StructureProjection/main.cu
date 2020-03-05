#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <cstdlib>
#include <math.h>
#include <sys/time.h>
#include <cuda_runtime.h>
#include "kernels.h"


using namespace std;

//************************************************************************************************************************************************
// This code projects the ROIs selected on a virtual EPID for every 0.5 degree and creates the Centroid.txt and the Results.txt files. Centroid.txt contains
//  the mean position of each projection and Results.txt contains the position of each points forming the contours of the projections.
//************************************************************************************************************************************************
int main (int argc, char **argv) 
{
    //~ time_t timer;
    //~ cout <<time(&timer)<<endl;
    //~ sleep(2);
    //~ cout <<time(&timer)<<endl;
    
    float *sourcePoint = new float[3];
    float *resolution = new float[3];
    float *isocenter = new float[3];
    float *refPointCT = new float[3];
    int *sens = new int[3];
    
    string PATH = argv[1];
    isocenter[0] = atof(argv[2]);
    isocenter[1] = atof(argv[3]);
    isocenter[2] = atof(argv[4]);
    sens[0] = atoi(argv[5]);
    sens[1] = atoi(argv[6]);
    sens[2] = atoi(argv[7]);
    string Patient_id = argv[8];
    resolution[0] = atof(argv[9]);
    resolution[1] = atof(argv[10]);
    resolution[2] = atof(argv[11]);
    refPointCT[0] = atof(argv[12]);
    refPointCT[1] = atof(argv[13]);
    refPointCT[2] = atof(argv[14]);
    int NbOfROIs = atoi(argv[15]);
    int NbRows = atoi(argv[16]);
    int NbCols = atoi(argv[17]);
    int NbSlices = atoi(argv[18]);
    string ROIName;
    struct timeval tp;
    long int start;
    long int end;
    int NbAngles = 720;
    
    int Xmin; int Xmax; int Ymin; int Ymax; int Zmin; int Zmax;
    
    int PanelNbPixels = 512;
    float PixDimEPID = 0.252*1024/PanelNbPixels*1.6;

    float BeamAngle = 0.0;
    float TableAngle = 0.0;
    float PI = 3.14159;
    
    int *Label = new int [NbSlices*NbRows*NbCols];
    int *im_EPID = new int [PanelNbPixels*PanelNbPixels];
    int *Panel = new int[PanelNbPixels*PanelNbPixels*NbAngles];
    
    for (int i = 0; i < PanelNbPixels*PanelNbPixels*NbAngles; i++) {
            Panel[i] = 0;
        }
    
    ifstream RoiFile;
    RoiFile.open("./listROI.txt");
    
    ofstream Centroid("./StructureProjection/Centroid.txt");
    ofstream Results("./StructureProjection/Results.txt");
    Results << NbOfROIs << "\t" << endl;
    Results << NbAngles << endl;
        
        
    for(int N=0; N<NbOfROIs; N++){
        
        RoiFile>>ROIName;
        RoiFile>>Xmin;RoiFile>>Xmax;RoiFile>>Ymin;RoiFile>>Ymax;RoiFile>>Zmin;RoiFile>>Zmax;
        
        Results << ROIName << endl;
        Centroid << ROIName << endl;
        
        streampos size =NbSlices*NbRows*NbCols;
        char * memblock; memblock = new char [size];
        
        
        
        ifstream myfile(("./ROIs/"+Patient_id+"."+ROIName).c_str(),ios::in|ios::binary);
        if (myfile.is_open()){
            myfile.read (memblock, size);
            myfile.close();
        }
        else{cout << "Unable to open file"<<endl;}
        int val;
        int pos = 0;
        for (int i = 0; i < NbSlices; i++) {
            for (int j = 0; j < NbRows; j++) {
                for (int k = 0; k < NbCols; k++) {
                    
                    
                    val = *(unsigned char *)&memblock[pos];
                    
                    Label[i*NbRows*NbCols+j*NbCols+k] = (int)val;
                    pos = pos + 1;
                }
            }
        }
        
        myfile.close();    
        delete[] memblock;
        

        
        //~ start = std::chrono::system_clock::now();
        
        cudaError_t err;
        size = NbSlices*NbRows*NbCols * sizeof(int);
        float *d_Label = NULL;
        err = cudaMalloc((void **)&d_Label, size);
        err = cudaMemcpy(d_Label, Label, size, cudaMemcpyHostToDevice);
        
        size = 3 * sizeof(float);
        float *d_resolution = NULL;
        err = cudaMalloc((void **)&d_resolution, size);
        err = cudaMemcpy(d_resolution, resolution, size, cudaMemcpyHostToDevice);

        
        float offsetX_dicom = (isocenter[0] - refPointCT[0])*sens[0];
        float offsetY_dicom = (isocenter[1] - refPointCT[1])*sens[1];
        float offsetZ_dicom = (isocenter[2] - refPointCT[2])*sens[2]+(NbSlices-1)*resolution[2];
        
        gettimeofday(&tp, NULL);
        start = tp.tv_sec * 1000 + tp.tv_usec / 1000;
        
        int threadsPerBlock = PanelNbPixels;
        int blocksPerGrid = PanelNbPixels;
        
        
        
        for(int z=0;z<NbAngles;z++){
        
            BeamAngle = (float)(z)*0.5;
            
            
            sourcePoint[0] = 1000 * sin(BeamAngle*PI / 180.0);
            sourcePoint[1] = -1000 * cos(BeamAngle*PI / 180.0);
            sourcePoint[2] = 0.0;
            
            for (int i = 0; i < PanelNbPixels*PanelNbPixels; i++) {
                im_EPID[i] = 0;
            }
            
            size = 3 * sizeof(float);
            float *d_sourcePoint = NULL;
            err = cudaMalloc((void **)&d_sourcePoint, size);
            err = cudaMemcpy(d_sourcePoint, sourcePoint, size, cudaMemcpyHostToDevice);
            
            size = PanelNbPixels*PanelNbPixels*sizeof(int);
            int *d_im_EPID = NULL;
            err = cudaMalloc((void **)&d_im_EPID, size);
            err = cudaMemcpy(d_im_EPID, im_EPID, size, cudaMemcpyHostToDevice);

            ProjectionGPU<< < blocksPerGrid, threadsPerBlock >> >(d_Label, d_im_EPID, d_sourcePoint, d_resolution, BeamAngle, NbRows, NbCols, NbSlices, PanelNbPixels, PixDimEPID, TableAngle, Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, offsetX_dicom, offsetY_dicom, offsetZ_dicom);
            
            size = PanelNbPixels*PanelNbPixels* sizeof(int);
            err = cudaMemcpy(im_EPID, d_im_EPID, size, cudaMemcpyDeviceToHost);
            //~ cout <<"err: "<< err << endl;
            float NbOfPoints=0;
            float mean_i = 0;
            float mean_j = 0;
            for(int i=0;i<PanelNbPixels;i++){
                for(int j=0;j<PanelNbPixels;j++){
                    if(im_EPID[i*PanelNbPixels + j] ==1){
                        NbOfPoints = NbOfPoints + 1;
                        mean_i = mean_i +i;
                        mean_j = mean_j +j;
                        if(i==0 or j==0 or i==PanelNbPixels-1 or j==PanelNbPixels-1){
                            Panel[z*PanelNbPixels*PanelNbPixels+(PanelNbPixels-1-j)*PanelNbPixels+i] = 1;
                        }
                        else{
                            if(im_EPID[(i+1)*PanelNbPixels + j]==1 and im_EPID[(i-1)*PanelNbPixels + j]==1 and im_EPID[i*PanelNbPixels + j+1]==1 and im_EPID[i*PanelNbPixels + j-1]==1 and im_EPID[(i+1)*PanelNbPixels + j+1]==1 and im_EPID[(i-1)*PanelNbPixels + j+1]==1 and im_EPID[(i+1)*PanelNbPixels + j-1]==1 and im_EPID[(i-1)*PanelNbPixels + j-1]==1){
                                Panel[z*PanelNbPixels*PanelNbPixels+(PanelNbPixels-1-j)*PanelNbPixels+i] = 0;  
                            }
                            else{Panel[z*PanelNbPixels*PanelNbPixels+(PanelNbPixels-1-j)*PanelNbPixels+i] = 1;}
                        }
                    }
                    else{Panel[z*PanelNbPixels*PanelNbPixels+(PanelNbPixels-1-j)*PanelNbPixels+i] = 0;}
                }
            }
            
            cudaFree(d_sourcePoint);
            cudaFree(d_im_EPID);
            
            mean_i = mean_i/NbOfPoints;
            mean_j = mean_j/NbOfPoints;
            Centroid << BeamAngle << "\t" << mean_i << "\t" << mean_j <<endl;
        }
        
        for (int z = 0; z < NbAngles; z++){
            vector<int> Contour_X;
            vector<int> Contour_Y;
                
            for (int x = 0; x < PanelNbPixels; x++){
                for (int y = 0; y < PanelNbPixels; y++){
                    if (Panel[z*PanelNbPixels*PanelNbPixels + y * PanelNbPixels + x] == 1){
                        Contour_X.push_back(x);
                        Contour_Y.push_back(y);
                    }
                }
            }
            
            for(int v=0;v<Contour_X.size();v++){
                    Results << Contour_X.at(v)*256.0/PanelNbPixels <<"\t" << Contour_Y.at(v)*256.0/PanelNbPixels <<"\t";
            }
            
            Results << endl;
            Contour_X.clear();
            Contour_Y.clear();
            
        }

        cudaFree(d_Label);
        cudaFree(d_resolution);    
        
        cout<<ROIName<<endl;
        
    }
    Centroid.close();
    Results.close();
    RoiFile.close();
        
    delete[] sourcePoint; sourcePoint = NULL;
    delete[] resolution; resolution = NULL;
    delete[] isocenter; isocenter = NULL;
    delete[] refPointCT; refPointCT = NULL;
    delete[] sens; sens = NULL;
    delete[] Label; Label = NULL;
    delete[] im_EPID; im_EPID = NULL;
    delete[] Panel; Panel = NULL;
    

    gettimeofday(&tp, NULL);
    end = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    cout<<end-start<<endl;
    
    
    
    cout<<"Fin du programme"<<endl;
    return 0;
}
//=============================================================================================================================================